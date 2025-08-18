<script>
	import { Icon } from '$lib/macro';
	import { Link } from '$lib/button';
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
		transition: gap var(--trans);
	}

	.link:hover {
		gap: 16px;
	}
</style>
