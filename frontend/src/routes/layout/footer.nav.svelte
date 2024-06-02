<script>
	import Link from '$lib/button/link.svelte';
</script>

<div class="block">
	<Link class="secondary" href="/">Home</Link>
	&#8226;
	<Link class="secondary" href="#about">About</Link>
	&#8226;
	<Link class="secondary" href="/post">Post</Link>
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
