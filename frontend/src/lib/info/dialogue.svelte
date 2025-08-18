<script>
	import { module } from '$lib/store.svelte.js';

	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';
	import { Row } from '$lib/layout';

	let title = module.value.title || 'Done';
	let status = module.value.status || 200;
	let message = module.value.message || 'The action was successful';
	let buttons = module.value.buttons || [];
</script>

<div
	class="title"
	class:good={status == 200}
	class:bad={status == 400}
	class:warning={status == 201}
>
	{#if status == 200}
		<Icon icon="200" size="24" />
	{:else if status == 400}
		<Icon icon="400" size="24" />
	{:else if status == 201}
		<Icon icon="201" size="24" />
	{/if}
	{title}
</div>
<div class="body">
	<div class="text">
		{@html message}
	</div>

	<Row --row-gap="8px">
		{#each buttons as x}
			<Button
				--button-width="100%"
				onclick={() => {
					x.fn();
				}}
			>
				{#if x.icon}
					<Icon icon={x.icon} />
				{/if}
				{x.name}
			</Button>
		{/each}
	</Row>
</div>

<style>
	.title {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		padding: var(--sp2);
		padding-right: var(--sp4);

		color: white;
		fill: currentColor;
		font-weight: 700;
		text-transform: capitalize;
	}

	.good {
		background-color: green;
	}
	.bad {
		background-color: red;
	}
	.warning {
		background-color: var(--yellow);
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
