<script>
	import { Button, RoundButton } from '$lib/button';
	import { IG } from '$lib/input';

	let { value = $bindable(), placeholder = 'Search', ondone } = $props();
	let value_rt = $derived(value);

	const submit = (val) => {
		if (val == value) return;

		value = val;
		ondone?.(value);
	};
</script>

<IG
	type="text"
	{placeholder}
	bind:value={value_rt}
	no_pad
	onkeypress={(e) => {
		if (e.key == 'Enter') {
			submit(value_rt);
		}
	}}
>
	{#snippet right()}
		<div class="right">
			{#if value || value_rt}
				<div class="close">
					<RoundButton
						--button-background-color-hover="red"
						icon="x"
						onclick={() => {
							if (!value) value_rt = '';
							submit('');
						}}
					></RoundButton>
				</div>
			{/if}

			<Button
				icon="search"
				--button-padding-x="0"
				--button-width="40px"
				--button-height="40px"
				onclick={() => submit(value_rt)}
				disabled={value == value_rt}
			></Button>
		</div>
	{/snippet}
</IG>

<style>
	.right {
		display: flex;
		align-items: center;
		margin-right: 4px;
		gap: 2px;
	}
	.close {
		margin-right: var(--sp1);
	}
</style>
