<script>
	import { Button } from '.';
	let { ...props } = $props();
</script>

<Button
	{...props}
	--button-padding-x="0"
	--button-width="32px"
	--button-height="32px"
	--button-border-radius="50%"
	--button-background-color="var(--round-background-color, var(--input))"
	--button-background-color-hover="var(--round-background-color-hover)"
	--button-outline-color="var(--round-outline-color, var(--input))"
></Button>
