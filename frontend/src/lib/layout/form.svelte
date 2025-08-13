<script>
	import { Note } from '$lib/info';
	let { title, error, children } = $props();
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<div class="ititle">{title}</div>
	<Note note={error} status="400" --note-margin-top="16px"></Note>
	{@render children()}
</form>

<style>
	form {
		padding: var(--form-padding, 24px);
	}
	.ititle {
		margin-bottom: 16px;
	}
</style>
