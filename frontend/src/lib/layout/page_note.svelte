<script>
	let { children } = $props();
</script>

<div class="empty">
	{@render children()}
</div>

<style>
	.empty {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: var(--sp2);

		height: 200px;
		border-radius: var(--sp0);
		padding: var(--sp2);

		background-color: var(--bg2);
		color: var(--ft2);
		text-align: center;
	}
</style>
