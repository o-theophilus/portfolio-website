<script>
	import { module, user } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	import Like from './engage.like.svelte';
	import Rating from './engage.rating.svelte';
	import Share from './engage.share.svelte';

	export let post;
	export let update;

	let my_rating = 0;
	const set_rating = (data) => {
		post = data;
		my_rating = 0;
		for (const x of post.ratings) {
			if (x.user_key == $user.key) {
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

	{#if $user.login}
		<Button
			size="small"
			primary={my_rating != 0}
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
			Rate{#if my_rating}: {my_rating}{/if}
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
