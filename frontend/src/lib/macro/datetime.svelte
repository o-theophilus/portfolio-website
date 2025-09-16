<script>
	import { onMount, onDestroy } from 'svelte';

	let { datetime, type = 'date_medium' } = $props();

	let dateObj = $derived(datetime ? new Date(datetime) : null);
	let timeAgo = $state('');

	function updateTimeAgo() {
		if (dateObj) {
			timeAgo = calculateTimeAgo(dateObj);
		}
	}

	let interval;
	onMount(() => {
		updateTimeAgo();
		interval = setInterval(updateTimeAgo, 60_000);
	});

	onDestroy(() => {
		clearInterval(interval);
	});

	export const DAYS_FULL = [
		'Sunday',
		'Monday',
		'Tuesday',
		'Wednesday',
		'Thursday',
		'Friday',
		'Saturday'
	];
	export const MONTHS_FULL = [
		'January',
		'February',
		'March',
		'April',
		'May',
		'June',
		'July',
		'August',
		'September',
		'October',
		'November',
		'December'
	];
	export const DAYS_SHORT = DAYS_FULL.map((m) => m.slice(0, 3));
	export const MONTHS_SHORT = MONTHS_FULL.map((m) => m.slice(0, 3));

	const ordinalSuffix = (i) => {
		const j = i % 10,
			k = i % 100;
		if (j === 1 && k !== 11) return i + 'st';
		if (j === 2 && k !== 12) return i + 'nd';
		if (j === 3 && k !== 13) return i + 'rd';
		return i + 'th';
	};

	function calculateTimeAgo(date) {
		const now = new Date();
		const diff = now - date;

		if (diff < 60_000) return 'just now';
		if (diff < 3_600_000) {
			const minutes = Math.floor(diff / 60_000);
			return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
		}
		if (diff < 86_400_000) {
			const hours = Math.floor(diff / 3_600_000);
			return `${hours} hour${hours > 1 ? 's' : ''} ago`;
		}
		if (diff < 2_592_000_000) {
			const days = Math.floor(diff / 86_400_000);
			return `${days} day${days > 1 ? 's' : ''} ago`;
		}
		return formatDate(date, 'date_numeric');
	}

	function formatDate(date, formatType) {
		switch (formatType) {
			case 'day_short':
				return DAYS_SHORT[date.getDay()];
			case 'day_full':
				return DAYS_FULL[date.getDay()];
			case 'month_short':
				return MONTHS_SHORT[date.getMonth()];
			case 'month_full':
				return MONTHS_FULL[date.getMonth()];
			case 'date_ordinal':
				return `${ordinalSuffix(date.getDate())} of ${MONTHS_FULL[date.getMonth()]} ${date.getFullYear()}`;
			case 'date_numeric':
				return [
					date.getDate().toString().padStart(2, '0'),
					(date.getMonth() + 1).toString().padStart(2, '0'),
					date.getFullYear()
				].join('/');
			case 'date_medium':
				return [
					date.getDate().toString().padStart(2, '0'),
					MONTHS_FULL[date.getMonth()],
					date.getFullYear()
				].join(' ');
			case 'date_named':
				return [
					date.getDate().toString().padStart(2, '0'),
					MONTHS_SHORT[date.getMonth()],
					date.getFullYear()
				].join('-');
			case 'time_period':
				return date.getHours() < 12 ? 'Morning' : date.getHours() < 16 ? 'Afternoon' : 'Evening';
			case 'time_12h':
				return (
					[
						(date.getHours() % 12 || 12).toString().padStart(2, '0'),
						date.getMinutes().toString().padStart(2, '0')
					].join(':') + (date.getHours() < 12 ? 'am' : 'pm')
				);
			case 'year':
				return date.getFullYear();
			default:
				return date.toString();
		}
	}
</script>

{#if dateObj}
	{#if type === 'ago'}
		{timeAgo}
	{:else}
		{formatDate(dateObj, type)}
	{/if}
{/if}
