<script>
	import { Icon, Spinner } from '$lib/macro';
	import { app } from '$lib/store.svelte.js';

	let { item, edata = $bindable() } = $props();
	let loading = $state(true);
	let like = $derived.by(() => {
		if (edata.user_like == 'like') return edata.like - edata.dislike + 1;
		if (edata.user_like == 'dislike') return edata.like - edata.dislike - 1;
		return edata.like - edata.dislike;
	});

	export const load = async () => {
		loading = true;

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/engagement/${item.key}`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		loading = false;
		resp = await resp.json();

		if (resp.status == 200) {
			edata.comment = resp.comment;
			edata.like = resp.like;
			edata.dislike = resp.dislike;
			edata.share = resp.share;
			edata.view = resp.view;
			edata.user_like = resp.user_like;
		}
	};
</script>

{#if loading}
	<Spinner active={loading} size="20" />
{:else}
	<div class="line info">
		<div class="line" title="view{edata.view > 1 ? 's' : ''}">
			<Icon icon="eye" size="12" />
			{edata.view}
		</div>
		<div class="line" title="comment{edata.comment > 1 ? 's' : ''}">
			<Icon icon="message-circle" size="12" />
			{edata.comment}
		</div>
		<div class="line" title="like{like > 1 ? 's' : ''}">
			<Icon icon="thumbs-up" size="12" />
			{like}
		</div>
		<div class="line" title="share{edata.share > 1 ? 's' : ''}">
			<Icon icon="share-2" size="12" />
			{edata.share}
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
		font-size: 0.8rem;
	}
</style>
