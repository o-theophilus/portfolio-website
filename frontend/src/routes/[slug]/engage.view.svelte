<script>
	import Icon from '$lib/icon.svelte';
	import Loading from '$lib/loading.svelte';

	export let post_key;
	let post;
	let loading = true;

	export const reset = () => {
		loading = true;
	};

	export const refresh = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/engagements/${post_key}`);
		resp = await resp.json();
		loading = false;
		if (resp.status == 200) {
			post = resp.post;
		}
	};
</script>

{#if loading}
	<Loading active={loading} size="20" />
{:else}
	<div class="line info">
		<div class="line">
			<Icon icon="visibility" />
			{post.view}
		</div>
		<div class="line">
			<Icon icon="comment" />
			{post.comment}
		</div>
		<div class="line">
			<Icon icon="thumb_up" />
			{post._like}
		</div>
		<div class="line">
			<Icon icon="hotel_class" />
			{parseFloat(post.rating)}{#if post.ratings.length != 0}|{post.ratings.length}{/if}
		</div>
		<div class="line">
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
