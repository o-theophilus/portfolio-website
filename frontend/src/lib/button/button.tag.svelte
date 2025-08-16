<script>
	import { Button } from '.';

	let { children, ...props } = $props();
</script>

<Button
	{...props}
	--button-height="24px"
	--button-border-radius="20px"
	--button-font-size="0.8rem"
	--button-font-weight="500"
	--button-background-color="var(--tag-background-color, var(--input))"
	--button-color="var(--tag-color, unset"
	--button-outline-color="var(--tag-outline-color, var(--input))"
>
	{@render children()}
</Button>
