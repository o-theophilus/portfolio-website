<script>
	import { slide } from 'svelte/transition';
	import { module, app } from '$lib/store.svelte.js';

	import { Button, Like } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Note } from '$lib/info';

	import Rating from './rating.svelte';
	import Share from './share.svelte';

	let { post, update } = $props();
	let error = $state({});

	let my_rating = $state(0);
	const set_rating = (data) => {
		post = data;
		my_rating = 0;
		for (const x of post.ratings) {
			if (x.user_key == app.user.key) {
				my_rating = x.rating;
				break;
			}
		}
	};

	set_rating(post);

	const submit_like = async (liked) => {
		error = {};

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/like/${post.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ like: liked })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			post = resp.post;
		} else {
			error = resp;
		}
	};
</script>

<hr />

<div class="line">
	{#if app.user.login}
		<Like
			like={post.like.length}
			dislike={post.dislike.length}
			onlike={() => {
				post.dislike = post.dislike.filter((e) => e != app.user.key);
				if (post.like.includes(app.user.key)) {
					post.like = post.like.filter((e) => e != app.user.key);
				} else {
					post.like.push(app.user.key);
				}
				submit_like(true);
			}}
			ondislike={() => {
				post.like = post.like.filter((e) => e != app.user.key);
				if (post.dislike.includes(app.user.key)) {
					post.dislike = post.dislike.filter((e) => e != app.user.key);
				} else {
					post.dislike.push(app.user.key);
				}
				submit_like(false);
			}}
		/>

		<Button
			size="small"
			primary={my_rating != 0}
			onclick={() => module.open(Rating, { post, update, set_rating })}
		>
			<Icon icon="star" />
			Rate{#if my_rating}: {my_rating}{/if}
		</Button>
	{/if}

	<Button size="small" onclick={() => module.open(Share, post)}>
		<Icon icon="share-2" />
		Share
	</Button>
</div>

{#if error.error}
	<div class="error" transition:slide>
		{error.error}
	</div>
{/if}

<style>
	hr {
		margin: var(--sp2) 0;
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp1);
	}

	.error {
		color: red;
		font-size: 0.8rem;
		margin-top: 16px;
	}
</style>
