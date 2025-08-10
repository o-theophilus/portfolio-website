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
		gap: var(--sp2);

		height: 200px;
		border-radius: var(--sp0);
		padding: var(--sp2);

		color: var(--ft2);
		text-align: center;
	}
</style>
