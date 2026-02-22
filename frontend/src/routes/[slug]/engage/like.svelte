<script>
	import { Like } from '$lib/button';
	import { app } from '$lib/store.svelte.js';

	let { post, engagement = $bindable() } = $props();

	let like = $derived.by(() => {
		if (engagement.user_reaction == 'like') return engagement.others_like + 1;
		return engagement.others_like;
	});
	let dislike = $derived.by(() => {
		if (engagement.user_reaction == 'dislike') return engagement.others_dislike + 1;
		return engagement.others_dislike;
	});

	const submit = async (reaction) => {
		if (reaction == engagement.user_reaction) {
			engagement.user_reaction = null;
		} else {
			engagement.user_reaction = reaction;
		}

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/like/${post.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ reaction })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			engagement.others_like = resp.others_like;
			engagement.others_dislike = resp.others_dislike;
			engagement.user_reaction = resp.user_reaction;
		} else {
			error = resp;
		}
	};
</script>

{#if app.login}
	<Like
		active={engagement.user_reaction}
		{like}
		{dislike}
		onlike={() => submit('like')}
		ondislike={() => submit('dislike')}
	/>
{/if}
