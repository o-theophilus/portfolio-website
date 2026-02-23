<script>
	import { Button } from '.';

	let { ...props } = $props();
</script>

<Button
	{...props}
	--button-height="24px"
	--button-border-radius="20px"
	--button-font-size="0.7rem"
	--button-font-weight="400"
	--button-background-color="var(--tag-background-color, var(--input))"
	--button-color="var(--tag-color, var(--ft2))"
	--button-outline-color="var(--tag-outline-color, var(--ol))"
></Button>
