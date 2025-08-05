<script>
	import { Link } from '$lib/button';
</script>

<div class="block">
	<Link href="/">Home</Link>
	&#8226;
	<Link href="/#about">About</Link>
	&#8226;
	<Link href="/post">Post</Link>
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
