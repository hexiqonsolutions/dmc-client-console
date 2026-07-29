"use client";

import { Bot, Loader2, Send, Sparkles, Trash2, X } from "lucide-react";
import { useEffect, useRef, useState, useTransition } from "react";
import { toast } from "sonner";

import {
  askCopilotAction,
  clearCopilotConversationAction,
} from "@/app/actions/ai";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";

type RailMessage = {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  created_at: string;
};

type CopilotRailProps = {
  open: boolean;
  onClose: () => void;
  openAiConfigured: boolean;
};

export function CopilotRail({
  open,
  onClose,
  openAiConfigured,
}: CopilotRailProps) {
  const [message, setMessage] = useState("");
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<RailMessage[]>([]);
  const [mode, setMode] = useState<"openai" | "guided" | null>(null);
  const [isPending, startTransition] = useTransition();
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isPending, open]);

  if (!open) {
    return null;
  }

  function submit() {
    const trimmed = message.trim();
    if (!trimmed || isPending) {
      return;
    }

    setMessage("");
    startTransition(async () => {
      const result = await askCopilotAction({
        conversationId,
        message: trimmed,
      });

      if (!result.success) {
        toast.error(result.error);
        setMessage(trimmed);
        return;
      }

      setConversationId(result.conversationId);
      setMessages(
        result.messages.filter(
          (item): item is RailMessage =>
            item.role === "user" ||
            item.role === "assistant" ||
            item.role === "system",
        ),
      );
      setMode(result.mode);
    });
  }

  return (
    <aside
      className="flex w-full max-w-full flex-col border-l border-border/80 bg-card/95 md:w-96"
      aria-label="AI Copilot"
    >
      <div className="flex items-center justify-between gap-2 border-b border-border/80 px-4 py-3">
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <Sparkles className="size-4 text-primary" aria-hidden />
            <p className="font-heading text-sm font-semibold tracking-tight">
              AI Copilot
            </p>
            <Badge variant="secondary">
              {openAiConfigured ? (mode === "openai" ? "Live" : "Ready") : "Guided"}
            </Badge>
          </div>
          <p className="mt-0.5 text-xs text-muted-foreground">
            Ask about clients, projects, and DM OS workflows.
          </p>
        </div>
        <div className="flex items-center gap-1">
          {conversationId ? (
            <Button
              type="button"
              variant="ghost"
              size="icon"
              className="cursor-pointer"
              aria-label="Clear conversation"
              disabled={isPending}
              onClick={() => {
                startTransition(async () => {
                  const result =
                    await clearCopilotConversationAction(conversationId);
                  if (!result.success) {
                    toast.error(result.error);
                    return;
                  }
                  setConversationId(null);
                  setMessages([]);
                  setMode(null);
                  toast.success("Conversation cleared");
                });
              }}
            >
              <Trash2 className="size-4" />
            </Button>
          ) : null}
          <Button
            type="button"
            variant="ghost"
            size="icon"
            className="cursor-pointer"
            aria-label="Close copilot"
            onClick={onClose}
          >
            <X className="size-4" />
          </Button>
        </div>
      </div>

      <div className="flex-1 space-y-3 overflow-y-auto px-4 py-4">
        {messages.length === 0 ? (
          <div className="rounded-xl border border-dashed border-border bg-muted/30 px-4 py-8 text-center">
            <div className="mx-auto mb-3 flex size-10 items-center justify-center rounded-full bg-accent text-accent-foreground">
              <Bot className="size-5" aria-hidden />
            </div>
            <p className="text-sm font-medium text-foreground">
              How can I help your agency today?
            </p>
            <p className="mt-1 text-xs text-muted-foreground">
              Try “How do I add a client?” or “Summarize my projects.”
            </p>
            {!openAiConfigured ? (
              <p className="mt-3 text-xs text-muted-foreground">
                Guided mode is on. Add `OPENAI_API_KEY` for full AI replies.
              </p>
            ) : null}
          </div>
        ) : (
          messages.map((item) => (
            <div
              key={item.id}
              className={cn(
                "rounded-lg px-3 py-2 text-sm whitespace-pre-wrap",
                item.role === "user"
                  ? "ml-6 bg-primary text-primary-foreground"
                  : "mr-6 bg-muted text-foreground",
              )}
            >
              {item.content}
            </div>
          ))
        )}
        {isPending ? (
          <div className="mr-6 flex items-center gap-2 rounded-lg bg-muted px-3 py-2 text-sm text-muted-foreground">
            <Loader2 className="size-4 animate-spin" aria-hidden />
            Thinking…
          </div>
        ) : null}
        <div ref={bottomRef} />
      </div>

      <form
        className="border-t border-border/80 p-4"
        onSubmit={(event) => {
          event.preventDefault();
          submit();
        }}
      >
        <LabelledComposer
          value={message}
          disabled={isPending}
          onChange={setMessage}
          onSubmit={submit}
        />
      </form>
    </aside>
  );
}

function LabelledComposer({
  value,
  disabled,
  onChange,
  onSubmit,
}: {
  value: string;
  disabled: boolean;
  onChange: (value: string) => void;
  onSubmit: () => void;
}) {
  return (
    <div className="space-y-2">
      <label htmlFor="copilot-message" className="sr-only">
        Message
      </label>
      <Textarea
        id="copilot-message"
        value={value}
        disabled={disabled}
        rows={3}
        placeholder="Ask Copilot…"
        onChange={(event) => onChange(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            onSubmit();
          }
        }}
      />
      <Button
        type="submit"
        className="w-full cursor-pointer"
        disabled={disabled || value.trim().length < 2}
      >
        {disabled ? (
          <>
            <Loader2 className="size-4 animate-spin" />
            Sending…
          </>
        ) : (
          <>
            <Send className="size-4" />
            Send
          </>
        )}
      </Button>
    </div>
  );
}
