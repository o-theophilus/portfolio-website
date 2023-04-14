<script>
	import { goto } from '$app/navigation';
	import { module } from '$lib/store.js';

	import SVG from '$lib/comp/svg.svelte';
	import Button from '$lib/comp/button.svelte';

	export let title;
	export let status;
	export let message;
	export let button = [];
</script>

<strong
	class="big"
	class:good={status == 'good'}
	class:bad={status == 'bad'}
	class:warning={status == 'warning'}
>
	{#if status == 'good'}
		<SVG type="check" size="20" />
	{:else if status == 'bad'}
		<SVG type="close" />
	{:else if status == 'warning'}
		<SVG type="info" size="20" />
	{/if}
	{title}
</strong>
<div class="body">
	<div class="text">
		{@html message}
	</div>
	<div class="row">
		{#each button as b}
			<Button
				name={b.name}
				icon={b.icon}
				class="wide"
				on:click={() => {
					b.fn();
				}}
			/>
		{/each}
	</div>
</div>

<style>
	strong {
		display: flex;
		align-items: center;
		gap: var(--gap2);

		padding: var(--gap2);
		padding-right: var(--gap5);
		color: var(--accent5_);
		fill: var(--accent5_);

		text-transform: capitalize;
	}

	.good {
		background-color: var(--color3);
	}
	.bad {
		background-color: var(--color2);
	}
	.warning {
		background-color: var(--color4);
	}
	.body {
		display: flex;
		flex-direction: column;
		gap: var(--gap2);

		padding: var(--gap2);
	}

	.text:first-letter {
		text-transform: uppercase;
	}
</style>
