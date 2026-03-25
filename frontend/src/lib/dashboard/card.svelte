<script>
	let { title, data = [], children } = $props();
</script>

<div class="card">
	<div class="title">
		{title}
	</div>

	{@render children?.()}
</div>

<style>
	.card {
		background-color: var(--bg3);
		padding: 16px;
		border-radius: 8px;
	}

	.title {
		font-weight: 800;
		font-size: 0.8rem;
	}
</style>
