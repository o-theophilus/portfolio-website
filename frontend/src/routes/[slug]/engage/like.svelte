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

		let response = await fetch(`${import.meta.env.VITE_BACKEND}/like/post/${post.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ reaction })
		});
		let result = await response.json();

		if (response.status == 200) {
			engagement.others_like = result.others_like;
			engagement.others_dislike = result.others_dislike;
			engagement.user_reaction = result.user_reaction;
		} else {
			error = result;
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
