<script>
	import Button from '$lib/button.svelte';
</script>

<div class="block">
	<Button class="secondary" href="/">Home</Button>
	&#8226;
	<Button class="secondary" href="/project">Project</Button>
	&#8226;
	<Button class="secondary" href="/blog">Blog</Button>
</div>

<style>
	.block {
		text-align: center;
	}
	@media screen and (min-width: 600px) {
		.block {
			text-align: unset;
		}
	}
</style>
