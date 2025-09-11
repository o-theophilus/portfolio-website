<script>
	import { Icon, Spinner } from '$lib/macro';

	let { key } = $props();
	let item = $state();
	let loading = $state(true);

	export const load = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/engagements/${key}`);
		resp = await resp.json();
		loading = false;
		if (resp.status == 200) {
			item = resp.item;
		}
	};
</script>

{#if loading}
	<Spinner active={loading} size="20" />
{:else}
	<div class="line info">
		<div class="line" title="view{item.view > 1 ? 's' : ''}">
			<Icon icon="eye" size="12" />
			{item.view}
		</div>
		<div class="line" title="comment{item.comment > 1 ? 's' : ''}">
			<Icon icon="message-circle" size="12" />
			{item.comment}
		</div>
		<div class="line" title="like{item._like > 1 ? 's' : ''}">
			<Icon icon="thumbs-up" size="12" />
			{item._like}
		</div>
		<div class="line" title="rating{item.ratings.length > 1 ? 's' : ''}">
			<Icon icon="star" size="12" />
			{parseFloat(item.rating)}{#if item.ratings.length != 0}|{item.ratings.length}{/if}
		</div>
		<div class="line" title="share{item.share > 1 ? 's' : ''}">
			<Icon icon="share-2" size="12" />
			{item.share}
		</div>
	</div>
{/if}

<style>
	.line {
		gap: 0;

		transition: color var(--trans);
	}

	.info {
		gap: 8px;
	}
</style>
