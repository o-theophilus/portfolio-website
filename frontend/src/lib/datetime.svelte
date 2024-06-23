<script>
	import { onMount } from 'svelte';

	export let datetime;
	export let type = 'date';
	export let style = '';

	$: if (datetime) {
		datetime = new Date(datetime);
	}

	export const days = [
		'Sunday',
		'Monday',
		'Tuesday',
		'Wednesday',
		'Thursday',
		'Friday',
		'Saturday'
	];
	export const days_short = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
	export const months = [
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
	export const ordinal_suffix_of = (i) => {
		var j = i % 10,
			k = i % 100;
		if (j == 1 && k != 11) {
			return i + 'st';
		}
		if (j == 2 && k != 12) {
			return i + 'nd';
		}
		if (j == 3 && k != 13) {
			return i + 'rd';
		}
		return i + 'th';
	};

	const timeAgo = (_date) => {
		let date = new Date(_date);
		const now = Date.now();
		const diff = now - date;

		if (diff < 60000) {
			return 'just now';
		} else if (diff < 3600000) {
			const minutes = Math.floor(diff / 60000);
			return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
		} else if (diff < 86400000) {
			const hours = Math.floor(diff / 3600000);
			return `${hours} hour${hours > 1 ? 's' : ''} ago`;
		} else if (diff < 2592000000) {
			const days = Math.floor(diff / 86400000);
			return `${days} day${days > 1 ? 's' : ''} ago`;
		} else {
			const year = date.getFullYear();
			const month = (date.getMonth() + 1).toString().padStart(2, '0');
			const day = date.getDate().toString().padStart(2, '0');
			return `${day}/${month}/${year}`;
		}
	};

	let time = timeAgo(datetime);
	onMount(() => {
		const intervalId = setInterval(() => {
			time = timeAgo(datetime);
		}, 1000);

		return () => clearInterval(intervalId);
	});
</script>

{#if datetime}
	{#if type == 'day'}
		{#if style == '1'}
			{days_short[datetime.getDay()]}
		{:else}
			{days[datetime.getDay()]}
		{/if}
	{/if}

	{#if type == 'date'}
		{#if style == '1'}
			{ordinal_suffix_of(datetime.getDate())} of
			{months[datetime.getMonth()]}
			{datetime.getFullYear()}
		{:else if style == '2'}
			{datetime.getDate().toString().padStart(2, '0')}/{datetime
				.getMonth()
				.toString()
				.padStart(2, '0')}/{datetime.getFullYear()}
		{:else if style == '3'}
			{datetime.getDate().toString().padStart(2, '0')}-{months[
				datetime.getMonth()
			]}-{datetime.getFullYear()}
		{:else}
			{datetime.getDate().toString().padStart(2, '0')}
			{months[datetime.getMonth()]}
			{datetime.getFullYear()}
		{/if}
	{/if}

	{#if type == 'time'}
		{#if style == '1'}
			{#if datetime.getHours() < 12}
				Morning
			{:else if datetime.getHours() < 16}
				Afternoon
			{:else}
				Evening
			{/if}
		{:else}
			{#if datetime.getHours() % 12}
				{(datetime.getHours() % 12).toString().padStart(2, '0')}{:else}12{/if}:{datetime
				.getMinutes()
				.toString()
				.padStart(2, '0')}{#if datetime.getHours() < 12}am{:else}pm {/if}
		{/if}
	{/if}

	{#if type == 'ago'}
		{time}
	{/if}
{/if}
