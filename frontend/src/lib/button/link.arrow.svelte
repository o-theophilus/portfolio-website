<script>
	import { Link } from '$lib/button';
	import { Icon } from '$lib/macro';
	let { children, ...props } = $props();
</script>

<Link {...props}>
	<div class="link">
		{@render children()}
		<Icon icon="arrow-right" />
	</div>
</Link>

<style>
	.link {
		display: inline-flex;
		align-items: center;
		gap: 8px;
		width: fit-content;
		transition: gap 0.2s ease-in-out;
	}

	.link:hover {
		gap: 16px;
	}
</style>
