<script>
	import { Button } from '.';

	let { ...props } = $props();
</script>

<Button
	{...props}
	--button-height="24px"
	--button-border-radius="20px"
	--button-font-size="0.8rem"
	--button-font-weight="500"
	--button-background-color="var(--tag-background-color, var(--input))"
	--button-outline-color="var(--tag-outline-color, var(--input))"
></Button>
