<script>
	let { error, block = false } = $props();
</script>

{#if error}
	<div class="error" class:block>
		{@html error}
	</div>
{/if}

<style>
	.error {
		color: red;
		font-size: 0.8rem;
		margin-top: var(--error-margin-top, 0);
		margin-bottom: var(--error-margin-bottom, 0);
	}

	.block {
		padding: 16px;

		margin-top: var(--error-margin-top, 16px);
		margin-bottom: var(--error-margin-bottom, 16px);
		background-color: rgba(255, 0, 0, 0.1);
		border-radius: 4px;
	}
</style>
