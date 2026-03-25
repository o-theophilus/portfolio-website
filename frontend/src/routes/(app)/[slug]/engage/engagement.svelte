<script>
	import { Icon, Spinner } from '$lib/macro';

	let { engagement, loading } = $props();

	let like = $derived.by(() => {
		let temp = engagement.others_like - engagement.others_dislike;
		if (engagement.user_reaction == 'like') return temp + 1;
		if (engagement.user_reaction == 'dislike') return temp - 1;

		return temp;
	});
</script>

{#if loading}
	<Spinner active={loading} size="20" />
{:else}
	<div class="line info">
		<div class="line" title="view{engagement.view > 1 ? 's' : ''}">
			<Icon icon="eye" size="12" />
			{engagement.view}
		</div>
		<div class="line" title="comment{engagement.comment > 1 ? 's' : ''}">
			<Icon icon="message-circle" size="12" />
			{engagement.comment}
		</div>
		<div class="line" title="like{like > 1 ? 's' : ''}">
			<Icon icon="thumbs-up" size="12" />
			{like}
		</div>
		<div class="line" title="share{engagement.share > 1 ? 's' : ''}">
			<Icon icon="share-2" size="12" />
			{engagement.share}
		</div>
	</div>
{/if}

<style>
	.line {
		gap: 0;

		transition: color 0.2s ease-in-out;
	}

	.info {
		gap: 8px;
		font-size: 0.8rem;
	}
</style>
