<script>
	import { Link } from '$lib/button';
	import { Icon } from '$lib/macro';
	let { children, ...props } = $props();
</script>

<Link {...props}>
	<div class="link">
		{@render children()}
		<div class="arrow">
			<Icon icon="arrow-right" />
		</div>
	</div>
</Link>

<style>
	.link {
		display: inline-flex;
		align-items: center;
		justify-content: center;

		gap: 4px;
		width: fit-content;

		&:hover .arrow {
			transform: translateX(8px);
		}

		& .arrow {
			display: flex;
			justify-content: center;
			align-items: center;

			transition: transform 0.2s ease-in-out;
		}
	}
</style>
