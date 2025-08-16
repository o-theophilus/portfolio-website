<script>
	import { Note } from '$lib/info';
	let { title, error, children } = $props();
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<div class="page_title">{title}</div>
	<Note note={error} status="400" --note-margin-top="16px"></Note>
	{@render children()}
</form>

<style>
	form {
		padding: var(--form-padding, 24px);
	}
	.page_title {
		margin-bottom: 16px;
	}
</style>
