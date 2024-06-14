<script>
	import { days, months, ordinal_suffix_of } from '$lib/store.js';

	export let datetime;
	export let type;
	export let style = '';

	$: if (datetime) {
		datetime = new Date(datetime);
	}
</script>

{#if datetime}
	{#if type == 'day'}
		{days[datetime.getDay()]}
	{/if}

	{#if type == 'date'}
		{#if style == 'a'}
			{ordinal_suffix_of(datetime.getDate())} of
			{months[datetime.getMonth()]}
			{datetime.getFullYear()}
		{:else}
			{datetime.getDate()}-{months[datetime.getMonth()]}-{datetime.getFullYear()}
		{/if}
	{/if}

	{#if type == 'time'}
		{#if style == 'a'}
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
{/if}
