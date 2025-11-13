<script>
	let { children } = $props();
</script>

<div class="bg">
	<section>
		{@render children()}
	</section>
</div>

<style>
	section {
		max-width: var(--content-width, var(--mobileWidth));
		width: 100%;
		margin: auto;
		padding: 0 24px;
		padding-top: var(--content-padding-top, 24px);
		padding-bottom: var(--content-padding-bottom, 24px);
		min-height: var(--content-height, calc(100vh - var(--headerHeight)));
	}

	.bg {
		background-color: var(--content-background-color, var(--bg1));
	}
</style>
