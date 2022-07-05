<script>
	import Marked from '$lib/marked.svelte';

	let md = `
\`\`\`javascript
console.log("here")
let a = 55;
\`\`\`
	`;
</script>

<h1>Marked</h1>

<div class="block">
	<textarea bind:value={md} />
	<div class="md"><Marked {md} /></div>
</div>

<style>
	.block {
		display: flex;
		max-width: calc(2 * var(--mobileWidth));

		margin: auto;
		padding: var(--pad);
	}

	textarea,
	.md {
		padding: var(--pad);
		width: 50%;

		resize: none;
		border: none;
	}
	textarea {
		background-color: rgb(255, 255, 175);
	}
</style>
