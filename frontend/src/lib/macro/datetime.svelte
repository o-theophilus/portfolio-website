<script>
	import { onDestroy, onMount } from 'svelte';
	import { formatDate, formatFullDateTime, formatTimeAgo, needsLiveUpdates } from './datetime';

	let { datetime, type = 'date_medium' } = $props();

	let date = datetime ? new Date(datetime) : null;
	let display = $state('');
	let interval = null;

	const update = () => {
		if (!date) return;

		display = type === 'ago' ? formatTimeAgo(date) : formatDate(date, type);

		// stop interval once it no longer needs updates
		if (interval && !needsLiveUpdates(date)) {
			clearInterval(interval);
			interval = null;
		}
	};

	onMount(() => {
		update();

		if (type === 'ago' && date && needsLiveUpdates(date)) {
			interval = setInterval(update, 60000);
		}
	});

	onDestroy(() => {
		if (interval) clearInterval(interval);
	});
</script>

{#if date}
	<time title={formatFullDateTime(date)} aria-label={display}>
		{display}
	</time>
{/if}

<style>
	time {
		line-height: 100%;
	}
</style>
