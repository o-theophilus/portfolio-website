<script>
	let type = 'content';
</script>

<div class="page {type}">
	<slot />
</div>

<style>
	.page {
		display: flex;
		flex-direction: column;
		gap:var(--gap2);
		max-width: var(--mobileWidth);
		min-height: 100vh;
		margin: auto;

		padding: var(--gap4);
		line-height: var(--lineHeight);
	}

	.content {
		padding-top: calc(var(--headerHeight) + var(--gap4));
	}
</style>
