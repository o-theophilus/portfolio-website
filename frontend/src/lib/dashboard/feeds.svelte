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
		margin-top: 8px;
		background-color: var(--bg3);
		padding: 16px;
		border-radius: 8px;
	}

	.title {
		font-weight: 800;
	}
</style>
