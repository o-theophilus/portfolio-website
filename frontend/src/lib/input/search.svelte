<script>
	import { Button, RoundButton } from '$lib/button';
	import { IG } from '$lib/input';
	import { Icon2 } from '$lib/macro';

	let {
		value = $bindable(),
		placeholder = 'Search',
		non_default = false,

		ondone
	} = $props();
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
						--button-background-color-hover="red"
						icon="x"
						onclick={() => {
							if (!value_submitted) {
								value = '';
								value_submitted = '';
							}
							submit('');
						}}
					></RoundButton>
				</div>
			{/if}

			{#if !non_default}
				<Button
					icon="search"
					--button-padding-x="0"
					--button-width="40px"
					--button-height="40px"
					onclick={() => {
						submit(value);
					}}
					disabled={value == value_submitted}
				></Button>
			{/if}
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
