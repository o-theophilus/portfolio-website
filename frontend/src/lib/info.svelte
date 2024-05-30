<script>
	import { module } from '$lib/store.js';

	import SVG from '$lib/svg.svelte';
	import Button from '$lib/button.svelte';

	let title = $module.title || 'Done';
	let status = $module.status || 200;
	let message = $module.message || 'The action was successful';
	let buttons = $module.buttons || [];
</script>

<div class="big" class:good={status == 200} class:bad={status == 400} class:warning={status == 201}>
	{#if status == 200}
		<SVG type="check" size="20" />
	{:else if status == 400}
		<SVG type="close" />
	{:else if status == 201}
		<SVG type="info" size="20" />
	{/if}
	{title}
</div>
<div class="body">
	<div class="text">
		{@html message}
	</div>
	<div class="line">
		{#each buttons as x}
			<Button
				name={x.name}
				icon={x.icon}
				class="wide"
				on:click={() => {
					x.fn();
				}}
			/>
		{/each}
	</div>
</div>

<style>
	.big {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		padding: var(--sp2);
		padding-right: var(--sp5);
		color: var(--ac5_);
		fill: var(--ac5_);

		text-transform: capitalize;
	}

	.good {
		background-color: var(--cl3);
	}
	.bad {
		background-color: var(--cl2);
	}
	.warning {
		background-color: var(--cl4);
	}
	.body {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);

		padding: var(--sp2);
	}

	.text:first-letter {
		text-transform: uppercase;
	}
</style>
