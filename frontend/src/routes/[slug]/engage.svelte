<script>
	import { module, user } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	import Like from './engage.like.svelte';
	import Rating from './engage.rating.svelte';
	import Share from './engage.share.svelte';

	export let post;
	export let update;

	let my_rating = null;
	const update_my_rating = async (data) => {
		my_rating = data;
	};
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
					post_key: post.key,
					my_rating,
					update_my_rating,
					update
				};
			}}
		>
			<Icon icon="hotel_class" />
			Rate: {parseFloat(post.rating)}/{post.ratings}
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
