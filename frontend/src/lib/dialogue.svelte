<script>
	import { module } from '$lib/store.js';

	import Icon from '$lib/icon.svelte';
	import Button from '$lib/button/button.svelte';

	let title = $module.title || 'Done';
	let status = $module.status || 200;
	let message = $module.message || 'The action was successful';
	let buttons = $module.buttons || [];
</script>

<div
	class="title"
	class:good={status == 200}
	class:bad={status == 400}
	class:warning={status == 201}
>
	{#if status == 200}
		<Icon icon="check_circle" />
	{:else if status == 400}
		<Icon icon="cancel" />
	{:else if status == 201}
		<Icon icon="error" />
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
				size="wide"
				on:click={() => {
					x.fn();
				}}
			>
				{#if x.icon}
					<Icon icon={x.icon} />
				{/if}
				{x.name}
			</Button>
		{/each}
	</div>
</div>

<style>
	.title {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		padding: var(--sp2);
		padding-right: var(--sp4);

		color: var(--ft1_b);
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
