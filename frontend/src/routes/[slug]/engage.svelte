<script>
	import { module, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';

	import Like from './engage.like.svelte';
	import Rating from './engage.rating.svelte';
	import Share from './engage.share.svelte';

	let { post, update } = $props();

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
</script>

<hr />

<div class="line">
	<Like
		name="post"
		entity={post}
		on:update={(e) => {
			update(e.detail.post);
		}}
	/>

	{#if app.user.login}
		<Button
			size="small"
			primary={my_rating != 0}
			onclick={() => module.open(Rating, { post, update, set_rating })}
		>
			<Icon icon="hotel_class" />
			Rate{#if my_rating}: {my_rating}{/if}
		</Button>
	{/if}

	<Button size="small" onclick={() => module.open(Share, post)}>
		<Icon icon="share" />
		Share
	</Button>
</div>

<style>
	hr {
		margin: var(--sp2) 0;
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp1);
	}
</style>
