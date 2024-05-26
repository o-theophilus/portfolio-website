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
	<div class="row">
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
