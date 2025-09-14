<script>
	import { app } from '$lib/store.svelte.js';
	import { Like } from '$lib/button';
	import { Spinner } from '$lib/macro';

	let { item, engagament } = $props();
	let loading = $state(true);
	let like = $state(0);
	let dislike = $state(0);
	let user_like = $state(null);
	let _like = $derived.by(() => {
		if (user_like == 'like') return like + 1;
		return like;
	});
	let _dislike = $derived.by(() => {
		if (user_like == 'dislike') return dislike + 1;
		return dislike;
	});

	export const load = async () => {
		loading = true;
		like = 0;
		dislike = 0;
		user_like = null;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/user_engagements/${item.key}`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		resp = await resp.json();
		loading = false;

		if (resp.status == 200) {
			like = resp.like;
			dislike = resp.dislike;
			user_like = resp.user_like;
		}
	};

	const submit = async (reaction) => {
		if (
			!user_like ||
			(reaction == 'like' && user_like == 'dislike') ||
			(reaction == 'dislike' && user_like == 'like')
		) {
			user_like = reaction;
		} else {
			user_like = null;
		}

		engagament.update({ like: _like - _dislike });

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
			like = resp.like;
			dislike = resp.dislike;
			user_like = resp.user_like;

			engagament.update({ like: _like - _dislike });
		} else {
			error = resp;
		}
	};
</script>

{#if app.login}
	{#if loading}
		<Spinner active={loading} size="20" />
	{:else}
		<Like
			active={user_like}
			like={_like}
			dislike={_dislike}
			onlike={() => submit('like')}
			ondislike={() => submit('dislike')}
		/>
	{/if}
{/if}
