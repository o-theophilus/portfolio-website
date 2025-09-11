<script>
	import { slide } from 'svelte/transition';
	import { module, app } from '$lib/store.svelte.js';

	import { Button, Like } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Note } from '$lib/info';

	import Rating from './rating.svelte';
	import Share from './share.svelte';

	let { item, update } = $props();
	let error = $state({});

	let my_rating = $state(0);
	const set_rating = (data) => {
		item = data;
		my_rating = 0;
		for (const x of item.ratings) {
			if (x.user_key == app.user.key) {
				my_rating = x.rating;
				break;
			}
		}
	};

	set_rating(item);

	const submit_like = async (liked) => {
		error = {};

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/like/${item.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ like: liked })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			item = resp.post;
		} else {
			error = resp;
		}
	};
</script>

<hr />

<div class="line">
	{#if app.login}
		<Like
			like={item.likes.length}
			dislike={item.dislikes.length}
			onlike={() => {
				item.dislikes = item.dislikes.filter((e) => e != app.user.key);
				if (item.likes.includes(app.user.key)) {
					item.likes = item.likes.filter((e) => e != app.user.key);
				} else {
					item.likes.push(app.user.key);
				}
				submit_like(true);
			}}
			ondislike={() => {
				item.likes = item.likes.filter((e) => e != app.user.key);
				if (item.dislikes.includes(app.user.key)) {
					item.dislikes = item.dislikes.filter((e) => e != app.user.key);
				} else {
					item.dislikes.push(app.user.key);
				}
				submit_like(false);
			}}
		/>

		<Button
			primary={my_rating != 0}
			onclick={() => module.open(Rating, { item, update, set_rating })}
		>
			<Icon icon="star" />
			Rate{#if my_rating}: {my_rating}{/if}
		</Button>
	{/if}

	<Button onclick={() => module.open(Share, { item })}>
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
