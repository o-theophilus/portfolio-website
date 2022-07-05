<script>
	export let noMargin = false;
</script>

<div class="pageContent" class:removeMargin={!noMargin} class:noMargin>
	<slot />
</div>

<style>
	.pageContent {
		max-width: var(--mobileWidth);
		margin: auto;

		padding: var(--headerHeight) var(--pad);
		line-height: var(--lineHeight);
	}
	.noMargin {
		padding-top: calc(var(--headerHeight) * 2);
	}
</style>
