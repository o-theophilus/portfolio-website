<script>
	import { Icon, Spinner } from '$lib/macro';

	let { post_key } = $props();
	let post = $state();
	let loading = $state(true);

	export const load = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/engagements/${post_key}`);
		resp = await resp.json();
		loading = false;
		if (resp.status == 200) {
			post = resp.post;
		}
	};
</script>

{#if loading}
	<Spinner active={loading} size="20" />
{:else}
	<div class="line info">
		<div class="line" title="view{post.view > 1 ? 's' : ''}">
			<Icon icon="visibility" />
			{post.view}
		</div>
		<div class="line" title="comment{post.comment > 1 ? 's' : ''}">
			<Icon icon="comment" />
			{post.comment}
		</div>
		<div class="line" title="like{post._like > 1 ? 's' : ''}">
			<Icon icon="thumb_up" />
			{post._like}
		</div>
		<div class="line" title="rating{post.ratings.length > 1 ? 's' : ''}">
			<Icon icon="hotel_class" />
			{parseFloat(post.rating)}{#if post.ratings.length != 0}|{post.ratings.length}{/if}
		</div>
		<div class="line" title="share{post.share > 1 ? 's' : ''}">
			<Icon icon="share" />
			{post.share}
		</div>
	</div>
{/if}

<style>
	.line {
		display: flex;
		align-items: center;
		gap: 2px;

		font-size: 0.8rem;
		color: var(--ft2);
		line-height: 1;

		transition: color var(--trans);
	}

	.info {
		gap: var(--sp1);
	}
</style>
