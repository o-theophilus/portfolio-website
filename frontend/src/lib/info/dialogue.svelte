<script>
	import { module } from '$lib/store.svelte.js';

	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';

	let title = module.value.title || 'Done';
	let status = module.value.status || 200;
	let message = module.value.message || 'The action was successful';
	let buttons = module.value.buttons || [];
</script>

<div class="title _{status}">
	<Icon
		icon={status == 400 ? 'circle-x' : status == 201 ? 'triangle-alert' : 'square-check'}
		size="20"
	/>
	{title}
</div>
<div class="text">
	{@html message}
</div>

{#if buttons.length}
	<div class="line btn">
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
	</div>
{/if}

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

	._200 {
		background-color: green;
	}
	._400 {
		background-color: red;
	}
	._201 {
		background-color: var(--yellow);
	}

	.text,
	.btn {
		padding: 0 var(--sp2);
		margin: var(--sp2) 0;
	}

	.text:first-letter {
		text-transform: uppercase;
	}
</style>
