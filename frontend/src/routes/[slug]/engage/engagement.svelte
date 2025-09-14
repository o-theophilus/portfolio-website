<script>
	import { Icon, Spinner } from '$lib/macro';
	import { app } from '$lib/store.svelte.js';

	let { item } = $props();
	let engagement = $state({
		comment: 0,
		like: 0,
		share: 0,
		view: 0
	});
	let loading = $state(true);

	export const update = (data) => {
		console.log(data);

		if ('like' in data) {
			engagement.like = data.like;
		}
	};

	export const load = async () => {
		loading = true;

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/engagement/${item.key}`);
		loading = false;
		resp = await resp.json();

		if (resp.status == 200) {
			engagement = resp;
		}
	};
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
		<div class="line" title="like{engagement.like > 1 ? 's' : ''}">
			<Icon icon="thumbs-up" size="12" />
			{engagement.like}
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

		transition: color var(--trans);
	}

	.info {
		gap: 8px;
		font-size: 0.8rem;
	}
</style>
