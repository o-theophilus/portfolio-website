<script>
	import { module, user } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	import Like from './engage.like.svelte';
	import Rating from './engage.rating.svelte';
	import Share from './engage.share.svelte';

	export let post;
	export let update;

	let rating = 0;
	const set_rating = (ratings) => {
		rating = 0;
		for (const x in ratings) {
			rating += ratings[x].rating;
		}
		if (rating != 0) {
			rating /= ratings.length;
		}
	};

	set_rating(post.ratings);
</script>

<hr />

<div class="line">
	<Like
		name="post"
		entity={post}
		on:update={(e) => {
			post = e.detail.post;
		}}
	/>

	{#if $user.login}
		<Button
			size="small"
			on:click={() => {
				$module = {
					module: Rating,
					post,
					update,
					set_rating
				};
			}}
		>
			<Icon icon="hotel_class" />
			Rate: {parseFloat(rating)} |
			<Icon icon="person" />
			{post.ratings.length}
		</Button>
	{/if}

	<Button
		size="small"
		on:click={() => {
			$module = {
				module: Share,
				post
			};
		}}
	>
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
