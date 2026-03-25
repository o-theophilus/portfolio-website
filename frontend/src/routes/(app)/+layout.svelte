<script>
	import { Footer, Nav } from '../_layout';
	let { children } = $props();
</script>

<Nav />
{@render children()}
<Footer />
