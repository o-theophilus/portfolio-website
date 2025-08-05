<script>
	let { space = false, nowrap = false, children } = $props();
</script>

<div class="row" class:space class:nowrap>
	{@render children()}
</div>

<style>
	.row {
		display: flex;
		align-items: center;
		gap: var(--row-gap, 16px);
		flex-wrap: wrap;
	}
	.space {
		justify-content: space-between;
	}
	.nowrap {
		flex-wrap: nowrap;
	}
</style>
