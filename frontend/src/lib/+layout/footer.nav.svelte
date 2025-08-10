<script>
	import { Link } from '$lib/button';
</script>

<div class="block">
	<Link --link-font-size="0.8rem" href="/">Home</Link>
	&#8226;
	<Link --link-font-size="0.8rem" href="/#about">About</Link>
	&#8226;
	<Link --link-font-size="0.8rem" href="/post">Post</Link>
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
