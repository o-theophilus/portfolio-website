<script>
	import { Button } from '.';

	let { children, ...props } = $props();
</script>

<Button
	{...props}
	--button-padding-x="0"
	--button-width="32px"
	--button-height="32px"
	--button-border-radius="50%"
	--button-color="var(--ft1)"
	--button-background-color="var(--bg2)"
	>
	{@render children()}
</Button>
