<script>
	import { app } from '$lib/store.svelte.js';
	import { Like } from '$lib/button';

	let { item, edata = $bindable() } = $props();

	let like = $derived.by(() => {
		if (edata.user_like == 'like') return edata.like + 1;
		return edata.like;
	});
	let dislike = $derived.by(() => {
		if (edata.user_like == 'dislike') return edata.dislike + 1;
		return edata.dislike;
	});

	const submit = async (reaction) => {
		if (
			!edata.user_like ||
			(reaction == 'like' && edata.user_like == 'dislike') ||
			(reaction == 'dislike' && edata.user_like == 'like')
		) {
			edata.user_like = reaction;
		} else {
			edata.user_like = null;
		}

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/like`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ entity_type: 'post', entity_key: item.key, reaction })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			edata.like = resp.like;
			edata.dislike = resp.dislike;
			edata.user_like = resp.user_like;
		} else {
			error = resp;
		}
	};
</script>

{#if app.login}
	<Like
		--like-background-color="var(--button-background-color)"
		--like-outline-color="var(--button-outline-color)"
		active={edata.user_like}
		{like}
		{dislike}
		onlike={() => submit('like')}
		ondislike={() => submit('dislike')}
	/>
{/if}
