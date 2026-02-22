<script>
	let { children } = $props();
</script>

<div class="note">
	{@render children()}
</div>

<style>
	.note {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: 16px;

		height: 200px;
		border-radius: 4px;
		padding: 16px;

		color: var(--ft2);
		text-align: center;
	}
</style>
