<script>
	import { Button, RoundButton } from '$lib/button';
	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';

	let { value = $bindable(), placeholder = 'Search', non_default = false, ondone } = $props();
	let value_submitted = $state();

	const submit = (val) => {
		if (val == value_submitted) return;

		ondone?.(val);
		set(val);
	};

	export const set = (val) => {
		value = val;
		value_submitted = val;
	};
</script>

<IG
	type="text"
	{placeholder}
	bind:value
	no_pad
	onkeypress={(e) => {
		if (e.key == 'Enter') {
			submit(value);
		}
	}}
>
	{#snippet right()}
		<div class="right">
			{#if value || value_submitted}
				<div class="close">
					<RoundButton
						onclick={() => {
							if (!value_submitted) {
								value = '';
								value_submitted = '';
							}
							submit('');
						}}
					>
						<Icon icon="close" size="1.2" />
					</RoundButton>
				</div>
			{/if}

			{#if !non_default}
				<Button
					--button-width="50px"
					--button-height="50px"
					onclick={() => {
						submit(value);
					}}
					disabled={value == value_submitted}
				>
					<Icon icon="search" size="1.5" />
				</Button>
			{/if}
		</div>
	{/snippet}
</IG>

<style>
	.right {
		display: flex;
		align-items: center;
		margin-right: 2px;
		gap: 2px;
	}
	.close {
		margin-right: var(--sp1);
	}
</style>
