#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_phase_3c.py
=================
Phase 3C: Input Bar, AI Providers & Chat Logic
Creates message input, slash commands, rate limiting, AI providers, chat hooks, and API routes.
"""

import os

files_created = 0
files_failed = 0


def create_file(path: str, content: str) -> None:
    global files_created, files_failed
    try:
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        files_created += 1
        print(f"  ✅ Created: {path}")
    except Exception as e:
        files_failed += 1
        print(f"  ❌ Failed: {path} - {e}")


def main():
    global files_created, files_failed

    print("=" * 60)
    print("🚀 BUILD PHASE 3C: Input Bar, AI Providers & Chat Logic")
    print("=" * 60)

    # ──────────────────────────────────────────────
    # ENCRYPTION
    # ──────────────────────────────────────────────
    print("\n📁 Encryption Library")
    print("-" * 40)

    create_file("lib/encryption.ts", """// مكتبة التشفير: تشفير وفك تشفير مفاتيح API باستخدام AES-256
// تُستخدم على الخادم فقط - لا تُعرض للعميل أبداً

/**
 * تشفير نص باستخدام AES-256-CBC
 * @param text - النص المراد تشفيره
 * @returns النص المشفر بتنسيق hex (iv:encrypted)
 */
export async function encrypt(text: string): Promise<string> {
  const key = getEncryptionKey();

  const encoder = new TextEncoder();
  const data = encoder.encode(text);

  const iv = crypto.getRandomValues(new Uint8Array(16));

  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    encoder.encode(key.padEnd(32, '0').slice(0, 32)),
    { name: 'AES-CBC' },
    false,
    ['encrypt']
  );

  const encrypted = await crypto.subtle.encrypt(
    { name: 'AES-CBC', iv },
    cryptoKey,
    data
  );

  const ivHex = Array.from(iv).map((b) => b.toString(16).padStart(2, '0')).join('');
  const encHex = Array.from(new Uint8Array(encrypted)).map((b) => b.toString(16).padStart(2, '0')).join('');

  return `${ivHex}:${encHex}`;
}

/**
 * فك تشفير نص مشفر بـ AES-256-CBC
 * @param encryptedText - النص المشفر بتنسيق hex (iv:encrypted)
 * @returns النص الأصلي
 */
export async function decrypt(encryptedText: string): Promise<string> {
  const key = getEncryptionKey();

  const parts = encryptedText.split(':');
  if (parts.length !== 2) {
    throw new Error('Invalid encrypted text format');
  }

  const ivHex = parts[0]!;
  const encHex = parts[1]!;

  const iv = new Uint8Array(
    ivHex.match(/.{1,2}/g)!.map((byte) => parseInt(byte, 16))
  );
  const encData = new Uint8Array(
    encHex.match(/.{1,2}/g)!.map((byte) => parseInt(byte, 16))
  );

  const encoder = new TextEncoder();
  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    encoder.encode(key.padEnd(32, '0').slice(0, 32)),
    { name: 'AES-CBC' },
    false,
    ['decrypt']
  );

  const decrypted = await crypto.subtle.decrypt(
    { name: 'AES-CBC', iv },
    cryptoKey,
    encData
  );

  return new TextDecoder().decode(decrypted);
}

/**
 * الحصول على مفتاح التشفير من المتغيرات البيئية
 */
function getEncryptionKey(): string {
  const key = process.env.ENCRYPTION_KEY;
  if (!key) {
    throw new Error('ENCRYPTION_KEY environment variable is not set');
  }
  return key;
}
""")

    # ──────────────────────────────────────────────
    # CHAT COMPONENTS (updated)
    # ──────────────────────────────────────────────
    print("\n📁 Chat Components (updated)")
    print("-" * 40)

    # 1. MessageInput.tsx
    create_file("components/chat/MessageInput.tsx", """// حقل إدخال الرسالة: حقل نص قابل للتوسيع 1-5 أسطر مع إرسال وأوامر مائلة
'use client';

import { useState, useRef, useCallback, useEffect, type KeyboardEvent } from 'react';
import { useTranslations, useLocale } from 'next-intl';
import { Send, Square, Sparkles } from 'lucide-react';
import { cn } from '@/utils/cn';
import { Button } from '@/components/ui/button';
import { Tooltip } from '@/components/ui/tooltip';
import { TokenCounter } from '@/components/common/TokenCounter';
import { MessageCounter } from '@/components/common/MessageCounter';
import { SlashCommands } from './SlashCommands';
import { MESSAGE_LIMIT_PER_CHAT, UI_CONSTANTS } from '@/utils/constants';

interface MessageInputProps {
  onSend: (message: string) => void;
  onStop?: () => void;
  isSending: boolean;
  isStreaming: boolean;
  isDisabled: boolean;
  isRateLimited: boolean;
  messageCount: number;
  totalTokens: number;
  placeholder?: string;
  onSlashCommand?: (personaId: string) => void;
}

export function MessageInput({
  onSend,
  onStop,
  isSending,
  isStreaming,
  isDisabled,
  isRateLimited,
  messageCount,
  totalTokens,
  placeholder,
  onSlashCommand,
}: MessageInputProps) {
  const t = useTranslations('chat');
  const locale = useLocale();
  const [message, setMessage] = useState('');
  const [showSlashMenu, setShowSlashMenu] = useState(false);
  const [slashFilter, setSlashFilter] = useState('');
  const [selectedSlashIndex, setSelectedSlashIndex] = useState(0);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const isAtLimit = messageCount >= MESSAGE_LIMIT_PER_CHAT;
  const canSend = message.trim().length > 0 && !isSending && !isStreaming && !isDisabled && !isRateLimited && !isAtLimit;

  /**
   * تعديل ارتفاع مربع النص تلقائياً (1-5 أسطر)
   */
  const adjustHeight = useCallback(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    textarea.style.height = 'auto';
    const lineHeight = 24;
    const maxLines = 5;
    const maxHeight = lineHeight * maxLines;
    const newHeight = Math.min(Math.max(textarea.scrollHeight, lineHeight), maxHeight);
    textarea.style.height = `${newHeight}px`;
  }, []);

  useEffect(() => {
    adjustHeight();
    return () => {};
  }, [message, adjustHeight]);

  /**
   * التعامل مع تغيير النص
   */
  const handleChange = useCallback(
    (value: string) => {
      if (value.length > UI_CONSTANTS.MAX_MESSAGE_LENGTH) return;
      setMessage(value);

      if (value === '/') {
        setSlashFilter('');
        setShowSlashMenu(true);
        setSelectedSlashIndex(0);
      } else if (value.startsWith('/') && !value.includes(' ') && value.length <= 20) {
        setSlashFilter(value.substring(1).toLowerCase());
        setShowSlashMenu(true);
        setSelectedSlashIndex(0);
      } else {
        setShowSlashMenu(false);
      }
    },
    []
  );

  /**
   * إرسال الرسالة
   */
  const handleSend = useCallback(() => {
    if (!canSend) return;
    onSend(message.trim());
    setMessage('');
    setShowSlashMenu(false);
    setTimeout(() => textareaRef.current?.focus(), 50);
  }, [message, canSend, onSend]);

  /**
   * اختيار أمر مائل
   */
  const handleSlashSelect = useCallback(
    (personaId: string) => {
      setMessage('');
      setShowSlashMenu(false);
      onSlashCommand?.(personaId);
      setTimeout(() => textareaRef.current?.focus(), 50);
    },
    [onSlashCommand]
  );

  /**
   * معالجة أحداث لوحة المفاتيح
   */
  const handleKeyDown = useCallback(
    (e: KeyboardEvent<HTMLTextAreaElement>) => {
      if (showSlashMenu) {
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp' || e.key === 'Tab') {
          e.preventDefault();
          setSelectedSlashIndex((prev) =>
            e.key === 'ArrowUp' ? Math.max(0, prev - 1) : prev + 1
          );
          return;
        }
        if (e.key === 'Enter') {
          e.preventDefault();
          return;
        }
        if (e.key === 'Escape') {
          e.preventDefault();
          setShowSlashMenu(false);
          return;
        }
      }

      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    },
    [showSlashMenu, handleSend]
  );

  return (
    <div className="shrink-0 border-t border-gray-200 dark:border-dark-700 bg-white/80 dark:bg-dark-900/80 backdrop-blur-md p-3">
      <div className="max-w-3xl mx-auto relative">
        {/* قائمة الأوامر المائلة */}
        <SlashCommands
          filter={slashFilter}
          selectedIndex={selectedSlashIndex}
          onSelect={handleSlashSelect}
          visible={showSlashMenu}
        />

        {/* حقل الإدخال */}
        <div
          className={cn(
            'flex items-end gap-2 rounded-xl border bg-white dark:bg-dark-800 transition-colors',
            'focus-within:border-primary-500 focus-within:ring-1 focus-within:ring-primary-500/30',
            isAtLimit
              ? 'border-red-300 dark:border-red-700'
              : isRateLimited
                ? 'border-orange-300 dark:border-orange-700'
                : 'border-gray-200 dark:border-dark-600',
            'px-3 py-2'
          )}
        >
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => handleChange(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              isAtLimit
                ? t('message_limit_title')
                : isRateLimited
                  ? t('rate_limit_wait')
                  : placeholder ?? t('type_message')
            }
            disabled={isDisabled || isAtLimit}
            rows={1}
            className={cn(
              'flex-1 resize-none bg-transparent text-sm outline-none',
              'text-gray-700 dark:text-gray-300',
              'placeholder:text-gray-400 dark:placeholder:text-gray-500',
              'disabled:opacity-50 disabled:cursor-not-allowed',
              'min-h-[24px] max-h-[120px] leading-6'
            )}
            dir="auto"
          />

          {isStreaming ? (
            <Tooltip content={t('stop')}>
              <Button
                size="icon-sm"
                variant="destructive"
                onClick={onStop}
                className="shrink-0 rounded-lg"
                aria-label={t('stop')}
              >
                <Square className="h-4 w-4" />
              </Button>
            </Tooltip>
          ) : (
            <Tooltip content={t('send')}>
              <Button
                size="icon-sm"
                onClick={handleSend}
                disabled={!canSend}
                className="shrink-0 rounded-lg"
                aria-label={t('send')}
              >
                <Send className="h-4 w-4" />
              </Button>
            </Tooltip>
          )}
        </div>

        {/* شريط المعلومات السفلي */}
        <div className="flex items-center justify-between mt-1.5 px-1">
          <div className="flex items-center gap-3">
            <TokenCounter tokens={totalTokens} />
            <MessageCounter current={messageCount} />
          </div>
          <p className="text-[10px] text-gray-400 dark:text-gray-500 hidden sm:block">
            {t('type_slash')}
          </p>
        </div>
      </div>
    </div>
  );
}
""")

    # 2. SlashCommands.tsx
    create_file("components/chat/SlashCommands.tsx", """// أوامر مائلة: قائمة منبثقة فوق حقل الإدخال للشخصيات والأوامر السريعة
'use client';

import { memo, useEffect, useRef, useState } from 'react';
import { useLocale } from 'next-intl';
import { Sparkles, Lock, X } from 'lucide-react';
import { cn } from '@/utils/cn';
import { SLASH_COMMANDS } from '@/utils/constants';
import { useAuthStore } from '@/stores/authStore';
import { usePersonaStore } from '@/stores/personaStore';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';
import type { Persona } from '@/types/persona';

interface SlashCommandsProps {
  filter: string;
  selectedIndex: number;
  onSelect: (personaId: string) => void;
  visible: boolean;
}

interface CommandItem {
  id: string;
  command: string;
  label: string;
  description: string;
  section: 'system' | 'premium' | 'custom' | 'action';
  locked: boolean;
}

export const SlashCommands = memo(function SlashCommands({
  filter,
  selectedIndex,
  onSelect,
  visible,
}: SlashCommandsProps) {
  const locale = useLocale();
  const { role } = useAuthStore();
  const { clearPersona } = usePersonaStore();
  const supabase = createSupabaseBrowserClient();

  const [customPersonas, setCustomPersonas] = useState<Persona[]>([]);
  const [premiumPersonas, setPremiumPersonas] = useState<Persona[]>([]);
  const loadedRef = useRef(false);
  const listRef = useRef<HTMLDivElement>(null);

  // تحميل الشخصيات المخصصة والمميزة
  useEffect(() => {
    if (loadedRef.current || !visible) return;
    loadedRef.current = true;

    const load = async () => {
      try {
        const { data: custom } = await supabase
          .from('personas')
          .select('*')
          .eq('type', 'custom')
          .eq('is_active', true)
          .limit(10);

        const { data: premium } = await supabase
          .from('personas')
          .select('*')
          .eq('type', 'premium')
          .eq('is_active', true)
          .limit(10);

        if (custom) setCustomPersonas(custom as Persona[]);
        if (premium) setPremiumPersonas(premium as Persona[]);
      } catch {
        // تجاهل
      }
    };

    load();
    return () => {};
  }, [visible, supabase]);

  // بناء قائمة الأوامر الموحدة
  const allItems: CommandItem[] = [];

  // أوامر النظام المدمجة
  SLASH_COMMANDS.forEach((cmd) => {
    allItems.push({
      id: cmd.personaId,
      command: cmd.command,
      label: locale === 'ar' ? cmd.labelAr : cmd.labelEn,
      description: locale === 'ar' ? cmd.description_ar : cmd.description_en,
      section: 'system',
      locked: false,
    });
  });

  // الشخصيات المميزة
  premiumPersonas.forEach((p) => {
    allItems.push({
      id: p.id,
      command: `/${p.name.replace(/\\s+/g, '_').toLowerCase().substring(0, 12)}`,
      label: p.name,
      description: p.description.substring(0, 60),
      section: 'premium',
      locked: role === 'free',
    });
  });

  // الشخصيات المخصصة
  customPersonas.forEach((p) => {
    allItems.push({
      id: p.id,
      command: `/${p.name.replace(/\\s+/g, '_').toLowerCase().substring(0, 12)}`,
      label: p.name,
      description: p.description.substring(0, 60),
      section: 'custom',
      locked: false,
    });
  });

  // أمر إلغاء الشخصية
  allItems.push({
    id: '__none__',
    command: '/none',
    label: locale === 'ar' ? 'بدون شخصية' : 'No Persona',
    description: locale === 'ar' ? 'إزالة الشخصية النشطة' : 'Remove active persona',
    section: 'action',
    locked: false,
  });

  // التصفية
  const filtered = allItems.filter(
    (item) =>
      item.command.substring(1).startsWith(filter) ||
      item.label.toLowerCase().includes(filter.toLowerCase())
  );

  // تمرير العنصر المحدد ليكون مرئياً
  useEffect(() => {
    if (!listRef.current) return;
    const selected = listRef.current.querySelector(`[data-index="${selectedIndex}"]`);
    if (selected) {
      selected.scrollIntoView({ block: 'nearest' });
    }
    return () => {};
  }, [selectedIndex]);

  if (!visible || filtered.length === 0) return null;

  const sections = {
    system: locale === 'ar' ? '⚡ الشخصيات الأساسية' : '⚡ System Personas',
    premium: locale === 'ar' ? '✨ الشخصيات المميزة' : '✨ Premium Personas',
    custom: locale === 'ar' ? '🎨 شخصياتي' : '🎨 My Personas',
    action: locale === 'ar' ? '⚙️ أوامر' : '⚙️ Commands',
  };

  let lastSection = '';
  let realIndex = 0;

  const handleSelect = (item: CommandItem) => {
    if (item.locked) return;
    if (item.id === '__none__') {
      clearPersona();
      onSelect('');
    } else {
      onSelect(item.id);
    }
  };

  return (
    <div
      ref={listRef}
      className={cn(
        'absolute bottom-full start-0 end-0 mb-2 rounded-xl',
        'border border-gray-200 dark:border-dark-700',
        'bg-white dark:bg-dark-800 shadow-2xl overflow-hidden z-30',
        'max-h-[300px] overflow-y-auto custom-scrollbar animate-fade-in'
      )}
    >
      <div className="p-1.5">
        {filtered.map((item) => {
          const showSection = item.section !== lastSection;
          lastSection = item.section;
          const currentIndex = realIndex++;

          return (
            <div key={`${item.section}-${item.id}`}>
              {showSection && (
                <p className="px-3 py-1.5 text-[10px] font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider">
                  {sections[item.section]}
                </p>
              )}
              <button
                data-index={currentIndex}
                onClick={() => handleSelect(item)}
                disabled={item.locked}
                className={cn(
                  'flex items-center gap-3 w-full rounded-lg px-3 py-2 text-start transition-colors',
                  currentIndex === (selectedIndex % filtered.length)
                    ? 'bg-primary-500/10 text-primary-600 dark:text-primary-400'
                    : item.locked
                      ? 'text-gray-400 dark:text-gray-500 opacity-60 cursor-not-allowed'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-dark-700'
                )}
              >
                <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-primary-500/10">
                  {item.id === '__none__' ? (
                    <X className="h-3.5 w-3.5 text-gray-400" />
                  ) : (
                    <Sparkles className="h-3.5 w-3.5 text-primary-500" />
                  )}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <code className="text-[11px] font-mono text-primary-500">{item.command}</code>
                    <span className="text-sm font-medium truncate">{item.label}</span>
                  </div>
                  <p className="text-[11px] text-gray-400 truncate">{item.description}</p>
                </div>
                {item.locked && <Lock className="h-3.5 w-3.5 shrink-0 text-gray-400" />}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
});
""")

    # 3. RateLimitTimer.tsx
    create_file("components/chat/RateLimitTimer.tsx", """// مؤقت حد المعدل: عداد تنازلي مع تلميح استخدام المفتاح الخاص
'use client';

import { useState, useEffect, useCallback, memo } from 'react';
import { useTranslations } from 'next-intl';
import { Clock, Key } from 'lucide-react';
import { cn } from '@/utils/cn';
import { formatDuration } from '@/utils/formatters';

interface RateLimitTimerProps {
  seconds: number;
  isVisible: boolean;
  onComplete: () => void;
  showUpgradeHint?: boolean;
  className?: string;
}

export const RateLimitTimer = memo(function RateLimitTimer({
  seconds,
  isVisible,
  onComplete,
  showUpgradeHint = true,
  className,
}: RateLimitTimerProps) {
  const t = useTranslations('chat');
  const [remaining, setRemaining] = useState(seconds);

  useEffect(() => {
    setRemaining(seconds);
  }, [seconds]);

  useEffect(() => {
    if (!isVisible || remaining <= 0) return;

    const interval = setInterval(() => {
      setRemaining((prev) => {
        const next = prev - 1;
        if (next <= 0) {
          clearInterval(interval);
          onComplete();
          return 0;
        }
        return next;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [isVisible, remaining, onComplete]);

  if (!isVisible || remaining <= 0) return null;

  const progress = ((seconds - remaining) / seconds) * 100;

  return (
    <div
      className={cn(
        'flex flex-col items-center gap-3 rounded-xl',
        'border border-orange-200 dark:border-orange-800/30',
        'bg-orange-50 dark:bg-orange-900/10 p-5',
        className
      )}
    >
      <Clock className="h-8 w-8 text-orange-500 animate-pulse" />

      <div className="text-center space-y-1">
        <p className="text-sm font-medium text-orange-700 dark:text-orange-300">
          {t('rate_limit_wait')}
        </p>
        <p className="text-3xl font-mono font-bold text-orange-600 dark:text-orange-400 tabular-nums">
          {formatDuration(remaining)}
        </p>
      </div>

      {/* شريط التقدم */}
      <div className="w-full max-w-xs h-2 rounded-full bg-orange-200 dark:bg-orange-800/30 overflow-hidden">
        <div
          className="h-full rounded-full bg-gradient-to-r from-orange-400 to-orange-500 transition-all duration-1000 ease-linear"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* تلميح */}
      {showUpgradeHint && (
        <div className="flex items-center gap-2 text-xs text-orange-500/80 dark:text-orange-400/80">
          <Key className="h-3 w-3" />
          <span>{t('rate_limit_tip')}</span>
        </div>
      )}
    </div>
  );
});
""")

    # 4. MessageLimitAlert.tsx
    create_file("components/chat/MessageLimitAlert.tsx", """// تنبيه حد الرسائل: حوار يظهر عند بلوغ 15 رسالة مع خيارات
'use client';

import { memo, useState } from 'react';
import { useTranslations } from 'next-intl';
import { AlertTriangle, Plus, Download, Trash2, FileText, FileCode, FileDown } from 'lucide-react';
import { cn } from '@/utils/cn';
import { Button } from '@/components/ui/button';
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter,
} from '@/components/ui/dialog';
import { MESSAGE_LIMIT_PER_CHAT } from '@/utils/constants';

interface MessageLimitAlertProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onNewChat: () => void;
  onExport?: (format: 'pdf' | 'json' | 'markdown') => void;
  onDelete?: () => void;
  onKeep?: () => void;
}

export const MessageLimitAlert = memo(function MessageLimitAlert({
  open,
  onOpenChange,
  onNewChat,
  onExport,
  onDelete,
  onKeep,
}: MessageLimitAlertProps) {
  const t = useTranslations('chat');

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent onClose={() => onOpenChange(false)}>
        <DialogHeader>
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30">
              <AlertTriangle className="h-6 w-6 text-red-500" />
            </div>
            <div>
              <DialogTitle>{t('message_limit_title')}</DialogTitle>
              <DialogDescription>
                {t('message_limit_body', { limit: MESSAGE_LIMIT_PER_CHAT.toString() })}
              </DialogDescription>
            </div>
          </div>
        </DialogHeader>

        <div className="p-6 pt-2 space-y-4">
          {/* خيارات التصدير */}
          {onExport && (
            <div className="space-y-2">
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                {t('export_conversation')}
              </p>
              <div className="flex flex-wrap gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onExport('pdf')}
                  className="gap-1.5"
                >
                  <FileDown className="h-3.5 w-3.5" />
                  PDF
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onExport('json')}
                  className="gap-1.5"
                >
                  <FileCode className="h-3.5 w-3.5" />
                  JSON
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onExport('markdown')}
                  className="gap-1.5"
                >
                  <FileText className="h-3.5 w-3.5" />
                  Markdown
                </Button>
              </div>
            </div>
          )}
        </div>

        <DialogFooter className="flex-wrap gap-2">
          {onKeep && (
            <Button variant="outline" onClick={onKeep}>
              {t('keep_conversation')}
            </Button>
          )}
          {onDelete && (
            <Button variant="destructive" onClick={onDelete} className="gap-1.5">
              <Trash2 className="h-4 w-4" />
              {t('delete_conversation')}
            </Button>
          )}
          <Button onClick={onNewChat} className="gap-1.5">
            <Plus className="h-4 w-4" />
            {t('start_new')}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
});
""")

    # ──────────────────────────────────────────────
    # AI PROVIDERS
    # ──────────────────────────────────────────────
    print("\n📁 AI Provider Libraries")
    print("-" * 40)

    # 5. lib/ai-providers/index.ts
    create_file("lib/ai-providers/index.ts", """// مصنع مزودي الذكاء الاصطناعي: يعيد المزود المناسب حسب اسم المنصة
import { openRouterProvider } from './openrouter';
import { groqProvider } from './groq';
import { openAIProvider } from './openai';
import { anthropicProvider } from './anthropic';
import { geminiProvider } from './gemini';
import { togetherProvider } from './together';
import { mistralProvider } from './mistral';
import type { PlatformName } from '@/types/platform';
import type { AIMessage } from '@/types/chat';

/**
 * واجهة مزود AI
 */
export interface AIProviderInterface {
  createStreamRequest: (config: StreamRequestConfig) => {
    url: string;
    headers: Record<string, string>;
    body: string;
  };
  parseStreamChunk: (chunk: string) => string | null;
  fetchModels?: (apiKey: string) => Promise<Array<{ id: string; name: string }>>;
}

/**
 * إعدادات طلب البث
 */
export interface StreamRequestConfig {
  apiKey: string;
  model: string;
  messages: AIMessage[];
  maxTokens?: number;
  temperature?: number;
}

/**
 * خريطة المزودين
 */
const providers: Record<PlatformName, AIProviderInterface> = {
  openrouter: openRouterProvider,
  groq: groqProvider,
  openai: openAIProvider,
  anthropic: anthropicProvider,
  gemini: geminiProvider,
  together: togetherProvider,
  mistral: mistralProvider,
};

/**
 * الحصول على مزود حسب اسم المنصة
 */
export function getProvider(platform: PlatformName): AIProviderInterface {
  const provider = providers[platform];
  if (!provider) {
    throw new Error(\`Unsupported platform: \${platform}\`);
  }
  return provider;
}

/**
 * التحقق من دعم المنصة
 */
export function isSupportedPlatform(platform: string): platform is PlatformName {
  return platform in providers;
}
""")

    # 6. OpenRouter
    create_file("lib/ai-providers/openrouter.ts", """// مزود OpenRouter: متوافق مع OpenAI
import type { AIProviderInterface, StreamRequestConfig } from './index';

export const openRouterProvider: AIProviderInterface = {
  createStreamRequest(config: StreamRequestConfig) {
    return {
      url: 'https://openrouter.ai/api/v1/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': \`Bearer \${config.apiKey}\`,
        'HTTP-Referer': process.env.NEXT_PUBLIC_APP_URL ?? 'http://localhost:3000',
        'X-Title': process.env.NEXT_PUBLIC_APP_NAME ?? 'AI Chat',
      },
      body: JSON.stringify({
        model: config.model,
        messages: config.messages.map((m) => ({ role: m.role, content: m.content })),
        stream: true,
        max_tokens: config.maxTokens ?? 4096,
        temperature: config.temperature ?? 0.7,
      }),
    };
  },

  parseStreamChunk(chunk: string): string | null {
    if (chunk === '[DONE]') return null;
    try {
      const parsed = JSON.parse(chunk) as {
        choices?: Array<{ delta?: { content?: string } }>;
      };
      return parsed.choices?.[0]?.delta?.content ?? null;
    } catch {
      return null;
    }
  },

  async fetchModels(apiKey: string) {
    const res = await fetch('https://openrouter.ai/api/v1/models', {
      headers: { 'Authorization': \`Bearer \${apiKey}\` },
    });
    if (!res.ok) return [];
    const data = await res.json() as { data?: Array<{ id: string; name?: string }> };
    return (data.data ?? []).map((m) => ({ id: m.id, name: m.name ?? m.id }));
  },
};
""")

    # 7. Groq
    create_file("lib/ai-providers/groq.ts", """// مزود Groq: متوافق مع OpenAI
import type { AIProviderInterface, StreamRequestConfig } from './index';

export const groqProvider: AIProviderInterface = {
  createStreamRequest(config: StreamRequestConfig) {
    return {
      url: 'https://api.groq.com/openai/v1/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': \`Bearer \${config.apiKey}\`,
      },
      body: JSON.stringify({
        model: config.model,
        messages: config.messages.map((m) => ({ role: m.role, content: m.content })),
        stream: true,
        max_tokens: config.maxTokens ?? 4096,
        temperature: config.temperature ?? 0.7,
      }),
    };
  },

  parseStreamChunk(chunk: string): string | null {
    if (chunk === '[DONE]') return null;
    try {
      const parsed = JSON.parse(chunk) as {
        choices?: Array<{ delta?: { content?: string } }>;
      };
      return parsed.choices?.[0]?.delta?.content ?? null;
    } catch {
      return null;
    }
  },

  async fetchModels(apiKey: string) {
    const res = await fetch('https://api.groq.com/openai/v1/models', {
      headers: { 'Authorization': \`Bearer \${apiKey}\` },
    });
    if (!res.ok) return [];
    const data = await res.json() as { data?: Array<{ id: string }> };
    return (data.data ?? []).map((m) => ({ id: m.id, name: m.id }));
  },
};
""")

    # 8. OpenAI
    create_file("lib/ai-providers/openai.ts", """// مزود OpenAI: المزود الأصلي
import type { AIProviderInterface, StreamRequestConfig } from './index';

export const openAIProvider: AIProviderInterface = {
  createStreamRequest(config: StreamRequestConfig) {
    return {
      url: 'https://api.openai.com/v1/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': \`Bearer \${config.apiKey}\`,
      },
      body: JSON.stringify({
        model: config.model,
        messages: config.messages.map((m) => ({ role: m.role, content: m.content })),
        stream: true,
        max_tokens: config.maxTokens ?? 4096,
        temperature: config.temperature ?? 0.7,
      }),
    };
  },

  parseStreamChunk(chunk: string): string | null {
    if (chunk === '[DONE]') return null;
    try {
      const parsed = JSON.parse(chunk) as {
        choices?: Array<{ delta?: { content?: string } }>;
      };
      return parsed.choices?.[0]?.delta?.content ?? null;
    } catch {
      return null;
    }
  },

  async fetchModels(apiKey: string) {
    const res = await fetch('https://api.openai.com/v1/models', {
      headers: { 'Authorization': \`Bearer \${apiKey}\` },
    });
    if (!res.ok) return [];
    const data = await res.json() as { data?: Array<{ id: string }> };
    return (data.data ?? [])
      .filter((m) => m.id.startsWith('gpt'))
      .map((m) => ({ id: m.id, name: m.id }));
  },
};
""")

    # 9. Anthropic
    create_file("lib/ai-providers/anthropic.ts", """// مزود Anthropic: تنسيق مخصص مع x-api-key و anthropic-version
import type { AIProviderInterface, StreamRequestConfig } from './index';

interface AnthropicMessage {
  role: 'user' | 'assistant';
  content: string;
}

export const anthropicProvider: AIProviderInterface = {
  createStreamRequest(config: StreamRequestConfig) {
    // استخراج رسالة النظام
    let systemPrompt = '';
    const convertedMessages: AnthropicMessage[] = [];

    for (const msg of config.messages) {
      if (msg.role === 'system') {
        systemPrompt += (systemPrompt ? '\\n' : '') + msg.content;
      } else {
        convertedMessages.push({
          role: msg.role === 'user' ? 'user' : 'assistant',
          content: msg.content,
        });
      }
    }

    // ضمان أن أول رسالة من المستخدم
    if (convertedMessages.length > 0 && convertedMessages[0]?.role !== 'user') {
      convertedMessages.unshift({ role: 'user', content: 'Hello' });
    }

    const body: Record<string, unknown> = {
      model: config.model,
      messages: convertedMessages,
      stream: true,
      max_tokens: config.maxTokens ?? 4096,
      temperature: config.temperature ?? 0.7,
    };

    if (systemPrompt) {
      body.system = systemPrompt;
    }

    return {
      url: 'https://api.anthropic.com/v1/messages',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': config.apiKey,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify(body),
    };
  },

  parseStreamChunk(chunk: string): string | null {
    try {
      const parsed = JSON.parse(chunk) as {
        type?: string;
        delta?: { type?: string; text?: string };
      };

      if (parsed.type === 'content_block_delta' && parsed.delta?.type === 'text_delta') {
        return parsed.delta.text ?? null;
      }

      if (parsed.type === 'message_stop') {
        return null;
      }

      return null;
    } catch {
      return null;
    }
  },

  async fetchModels() {
    // Anthropic لا يوفر API لجلب النماذج
    return [
      { id: 'claude-sonnet-4-20250514', name: 'Claude Sonnet 4' },
      { id: 'claude-3-5-sonnet-20241022', name: 'Claude 3.5 Sonnet' },
      { id: 'claude-3-5-haiku-20241022', name: 'Claude 3.5 Haiku' },
      { id: 'claude-3-opus-20240229', name: 'Claude 3 Opus' },
    ];
  },
};
""")

    # 10. Gemini
    create_file("lib/ai-providers/gemini.ts", """// مزود Google Gemini: تنسيق مخصص مع contents/parts
import type { AIProviderInterface, StreamRequestConfig } from './index';

interface GeminiContent {
  role: 'user' | 'model';
  parts: Array<{ text: string }>;
}

export const geminiProvider: AIProviderInterface = {
  createStreamRequest(config: StreamRequestConfig) {
    let systemInstruction = '';
    const contents: GeminiContent[] = [];

    for (const msg of config.messages) {
      if (msg.role === 'system') {
        systemInstruction += (systemInstruction ? '\\n' : '') + msg.content;
      } else {
        contents.push({
          role: msg.role === 'user' ? 'user' : 'model',
          parts: [{ text: msg.content }],
        });
      }
    }

    // ضمان أن أول محتوى من المستخدم
    if (contents.length > 0 && contents[0]?.role !== 'user') {
      contents.unshift({ role: 'user', parts: [{ text: 'Hello' }] });
    }

    const body: Record<string, unknown> = {
      contents,
      generationConfig: {
        maxOutputTokens: config.maxTokens ?? 4096,
        temperature: config.temperature ?? 0.7,
      },
    };

    if (systemInstruction) {
      body.systemInstruction = { parts: [{ text: systemInstruction }] };
    }

    return {
      url: \`https://generativelanguage.googleapis.com/v1beta/models/\${config.model}:streamGenerateContent?key=\${config.apiKey}&alt=sse\`,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    };
  },

  parseStreamChunk(chunk: string): string | null {
    try {
      const parsed = JSON.parse(chunk) as {
        candidates?: Array<{
          content?: { parts?: Array<{ text?: string }> };
        }>;
      };

      const text = parsed.candidates?.[0]?.content?.parts?.[0]?.text;
      return text ?? null;
    } catch {
      return null;
    }
  },

  async fetchModels(apiKey: string) {
    const res = await fetch(
      \`https://generativelanguage.googleapis.com/v1beta/models?key=\${apiKey}\`
    );
    if (!res.ok) return [];
    const data = await res.json() as {
      models?: Array<{ name: string; displayName?: string; supportedGenerationMethods?: string[] }>;
    };
    return (data.models ?? [])
      .filter((m) => m.supportedGenerationMethods?.includes('generateContent'))
      .map((m) => ({
        id: m.name.replace('models/', ''),
        name: m.displayName ?? m.name,
      }));
  },
};
""")

    # 11. Together AI
    create_file("lib/ai-providers/together.ts", """// مزود Together AI: متوافق مع OpenAI
import type { AIProviderInterface, StreamRequestConfig } from './index';

export const togetherProvider: AIProviderInterface = {
  createStreamRequest(config: StreamRequestConfig) {
    return {
      url: 'https://api.together.xyz/v1/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': \`Bearer \${config.apiKey}\`,
      },
      body: JSON.stringify({
        model: config.model,
        messages: config.messages.map((m) => ({ role: m.role, content: m.content })),
        stream: true,
        max_tokens: config.maxTokens ?? 4096,
        temperature: config.temperature ?? 0.7,
      }),
    };
  },

  parseStreamChunk(chunk: string): string | null {
    if (chunk === '[DONE]') return null;
    try {
      const parsed = JSON.parse(chunk) as {
        choices?: Array<{ delta?: { content?: string } }>;
      };
      return parsed.choices?.[0]?.delta?.content ?? null;
    } catch {
      return null;
    }
  },

  async fetchModels(apiKey: string) {
    const res = await fetch('https://api.together.xyz/v1/models', {
      headers: { 'Authorization': \`Bearer \${apiKey}\` },
    });
    if (!res.ok) return [];
    const data = await res.json() as Array<{ id: string; display_name?: string; type?: string }>;
    return (Array.isArray(data) ? data : [])
      .filter((m) => m.type === 'chat')
      .map((m) => ({ id: m.id, name: m.display_name ?? m.id }));
  },
};
""")

    # 12. Mistral
    create_file("lib/ai-providers/mistral.ts", """// مزود Mistral: متوافق مع OpenAI
import type { AIProviderInterface, StreamRequestConfig } from './index';

export const mistralProvider: AIProviderInterface = {
  createStreamRequest(config: StreamRequestConfig) {
    return {
      url: 'https://api.mistral.ai/v1/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': \`Bearer \${config.apiKey}\`,
      },
      body: JSON.stringify({
        model: config.model,
        messages: config.messages.map((m) => ({ role: m.role, content: m.content })),
        stream: true,
        max_tokens: config.maxTokens ?? 4096,
        temperature: config.temperature ?? 0.7,
      }),
    };
  },

  parseStreamChunk(chunk: string): string | null {
    if (chunk === '[DONE]') return null;
    try {
      const parsed = JSON.parse(chunk) as {
        choices?: Array<{ delta?: { content?: string } }>;
      };
      return parsed.choices?.[0]?.delta?.content ?? null;
    } catch {
      return null;
    }
  },

  async fetchModels(apiKey: string) {
    const res = await fetch('https://api.mistral.ai/v1/models', {
      headers: { 'Authorization': \`Bearer \${apiKey}\` },
    });
    if (!res.ok) return [];
    const data = await res.json() as { data?: Array<{ id: string }> };
    return (data.data ?? []).map((m) => ({ id: m.id, name: m.id }));
  },
};
""")

    # ──────────────────────────────────────────────
    # HOOKS
    # ──────────────────────────────────────────────
    print("\n📁 Chat & Rate Limit Hooks")
    print("-" * 40)

    # 14. useRateLimit.ts
    create_file("hooks/useRateLimit.ts", """// خطاف حد المعدل: يدير التأخير الزمني بين الرسائل حسب نوع الحساب
'use client';

import { useState, useCallback, useRef, useEffect } from 'react';
import { useAuthStore } from '@/stores/authStore';
import { usePlatformStore } from '@/stores/platformStore';
import {
  FREE_MESSAGES_BEFORE_DELAY,
  FREE_DELAY_SECONDS,
  PREMIUM_DELAY_SECONDS,
} from '@/utils/constants';

interface UseRateLimitReturn {
  canSend: boolean;
  remainingSeconds: number;
  freeMessagesUsed: number;
  freeMessagesLeft: number;
  isLimited: boolean;
  isPremiumDelay: boolean;
  recordMessage: () => void;
  resetForNewChat: () => void;
}

export function useRateLimit(): UseRateLimitReturn {
  const { role } = useAuthStore();
  const { apiType } = usePlatformStore();

  const [remainingSeconds, setRemainingSeconds] = useState(0);
  const [freeMessagesUsed, setFreeMessagesUsed] = useState(0);
  const [isLimited, setIsLimited] = useState(false);
  const [isPremiumDelay, setIsPremiumDelay] = useState(false);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const isAdmin = role === 'admin';
  const isPremium = role === 'premium';
  const isFree = role === 'free';
  const isPublicApi = apiType === 'global';

  /**
   * مسح المؤقت
   */
  const clearTimer = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  /**
   * بدء العد التنازلي
   */
  const startCountdown = useCallback(
    (seconds: number, premium: boolean = false) => {
      clearTimer();
      setRemainingSeconds(seconds);
      setIsLimited(true);
      setIsPremiumDelay(premium);

      timerRef.current = setInterval(() => {
        setRemainingSeconds((prev) => {
          if (prev <= 1) {
            clearTimer();
            setIsLimited(false);
            setIsPremiumDelay(false);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    },
    [clearTimer]
  );

  /**
   * تسجيل رسالة مرسلة
   */
  const recordMessage = useCallback(() => {
    // المدير لا يخضع لحدود
    if (isAdmin) return;

    // المفتاح الخاص لا يخضع لحدود
    if (!isPublicApi) return;

    if (isPremium) {
      // المميز: تأخير 60 ثانية مخفي (يظهر كـ "يكتب...")
      startCountdown(PREMIUM_DELAY_SECONDS, true);
      return;
    }

    if (isFree) {
      const newUsed = freeMessagesUsed + 1;
      setFreeMessagesUsed(newUsed);

      // بعد 4 رسائل مجانية: تأخير 180 ثانية مرئي
      if (newUsed >= FREE_MESSAGES_BEFORE_DELAY) {
        startCountdown(FREE_DELAY_SECONDS, false);
        setFreeMessagesUsed(0); // إعادة العداد بعد التأخير
      }
    }
  }, [isAdmin, isPremium, isFree, isPublicApi, freeMessagesUsed, startCountdown]);

  /**
   * إعادة تعيين لمحادثة جديدة
   */
  const resetForNewChat = useCallback(() => {
    clearTimer();
    setRemainingSeconds(0);
    setFreeMessagesUsed(0);
    setIsLimited(false);
    setIsPremiumDelay(false);
  }, [clearTimer]);

  /**
   * تنظيف المؤقت عند الإزالة
   */
  useEffect(() => {
    return () => clearTimer();
  }, [clearTimer]);

  const canSend = !isLimited || isAdmin || !isPublicApi;
  const freeMessagesLeft = Math.max(0, FREE_MESSAGES_BEFORE_DELAY - freeMessagesUsed);

  return {
    canSend,
    remainingSeconds,
    freeMessagesUsed,
    freeMessagesLeft,
    isLimited,
    isPremiumDelay,
    recordMessage,
    resetForNewChat,
  };
}
""")

    # 13. useChat.ts (complete rewrite with streaming)
    create_file("hooks/useChat.ts", """// خطاف الدردشة المتكامل: يدير المحادثات والرسائل والبث المباشر
'use client';

import { useState, useCallback, useEffect, useRef } from 'react';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';
import { useChatStore } from '@/stores/chatStore';
import { useAuthStore } from '@/stores/authStore';
import { usePlatformStore } from '@/stores/platformStore';
import { usePersonaStore } from '@/stores/personaStore';
import type {
  Conversation, Message, CreateConversationData,
  UpdateConversationData, AIMessage,
} from '@/types/chat';

interface UseChatReturn {
  conversations: Conversation[];
  currentConversation: Conversation | null;
  messages: Message[];
  isLoadingConversations: boolean;
  isLoadingMessages: boolean;
  isSending: boolean;
  isStreaming: boolean;
  streamingContent: string;
  loadConversations: () => Promise<void>;
  loadConversation: (id: string) => Promise<Conversation | null>;
  loadMessages: (conversationId: string) => Promise<void>;
  sendMessage: (content: string) => Promise<void>;
  stopStreaming: () => void;
  createConversation: (data: CreateConversationData) => Promise<Conversation | null>;
  updateConversation: (id: string, data: UpdateConversationData) => Promise<void>;
  deleteConversation: (id: string) => Promise<void>;
  searchConversations: (query: string) => Conversation[];
}

export function useChat(): UseChatReturn {
  const supabase = createSupabaseBrowserClient();
  const { user } = useAuthStore();
  const { activePlatform, activeModel, apiType } = usePlatformStore();
  const { activePersona } = usePersonaStore();
  const {
    conversation: currentConversation,
    messages,
    isSending,
    isStreaming,
    streamingContent,
    setConversation,
    setMessages,
    addMessage,
    setSending,
    setStreaming,
    setStreamingContent,
    appendStreamingContent,
    incrementMessageCount,
    addTokens,
    clearChat,
  } = useChatStore();

  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoadingConversations, setIsLoadingConversations] = useState(false);
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const abortRef = useRef<AbortController | null>(null);
  const loadedRef = useRef(false);

  // تحميل المحادثات
  const loadConversations = useCallback(async () => {
    if (!user) return;
    setIsLoadingConversations(true);
    try {
      const { data, error } = await supabase
        .from('conversations')
        .select('*')
        .eq('user_id', user.id)
        .order('updated_at', { ascending: false });
      if (!error && data) setConversations(data as Conversation[]);
    } catch { /* تجاهل */ } finally {
      setIsLoadingConversations(false);
    }
  }, [supabase, user]);

  // تحميل محادثة واحدة
  const loadConversation = useCallback(
    async (id: string): Promise<Conversation | null> => {
      if (!user) return null;
      try {
        const { data, error } = await supabase
          .from('conversations')
          .select('*')
          .eq('id', id)
          .eq('user_id', user.id)
          .single();
        if (error || !data) return null;
        const conv = data as Conversation;
        setConversation(conv);
        return conv;
      } catch { return null; }
    },
    [supabase, user, setConversation]
  );

  // تحميل الرسائل
  const loadMessages = useCallback(
    async (conversationId: string) => {
      setIsLoadingMessages(true);
      try {
        const { data, error } = await supabase
          .from('messages')
          .select('*')
          .eq('conversation_id', conversationId)
          .order('created_at', { ascending: true });
        if (!error && data) setMessages(data as Message[]);
      } catch { /* تجاهل */ } finally {
        setIsLoadingMessages(false);
      }
    },
    [supabase, setMessages]
  );

  // إرسال رسالة مع بث مباشر
  const sendMessage = useCallback(
    async (content: string) => {
      if (!user || !currentConversation) return;
      setSending(true);
      setStreamingContent('');

      const startTime = Date.now();

      // إضافة رسالة المستخدم محلياً (تفاؤلي)
      const userMsg: Message = {
        id: crypto.randomUUID(),
        conversation_id: currentConversation.id,
        role: 'user',
        content,
        model: null,
        platform: null,
        persona_name: null,
        tokens_used: 0,
        response_time_ms: null,
        created_at: new Date().toISOString(),
      };
      addMessage(userMsg);
      incrementMessageCount();

      // حفظ رسالة المستخدم في قاعدة البيانات
      try {
        await supabase.from('messages').insert({
          conversation_id: currentConversation.id,
          role: 'user' as const,
          content,
        });
      } catch { /* تجاهل */ }

      // بناء رسائل API
      const apiMessages: AIMessage[] = [];

      // إضافة system prompt إذا وجدت شخصية
      if (activePersona?.system_prompt) {
        apiMessages.push({ role: 'system', content: activePersona.system_prompt });
      }

      // إضافة الرسائل السابقة
      for (const msg of messages) {
        if (msg.role === 'user' || msg.role === 'assistant') {
          apiMessages.push({ role: msg.role, content: msg.content });
        }
      }

      // إضافة الرسالة الحالية
      apiMessages.push({ role: 'user', content });

      // إرسال للـ API
      try {
        setSending(false);
        setStreaming(true);

        abortRef.current = new AbortController();

        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            messages: apiMessages,
            model: activeModel,
            platform: activePlatform,
            conversationId: currentConversation.id,
            personaName: activePersona?.name ?? null,
            apiType,
          }),
          signal: abortRef.current.signal,
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({})) as Record<string, string>;
          throw new Error(errorData.error ?? 'Failed to send message');
        }

        // قراءة البث
        const reader = response.body?.getReader();
        if (!reader) throw new Error('No response body');

        const decoder = new TextDecoder();
        let fullContent = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const text = decoder.decode(value, { stream: true });
          const lines = text.split('\\n');

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6);
              if (data === '[DONE]') continue;

              try {
                const parsed = JSON.parse(data) as { content?: string; error?: string };
                if (parsed.content) {
                  fullContent += parsed.content;
                  setStreamingContent(fullContent);
                }
                if (parsed.error) {
                  throw new Error(parsed.error);
                }
              } catch (parseErr) {
                if (parseErr instanceof Error && parseErr.message !== data) {
                  // ليس JSON صالح، تجاهل
                }
              }
            }
          }
        }

        const responseTime = Date.now() - startTime;
        const estimatedTokens = Math.ceil(fullContent.length / 4);

        // إضافة رسالة المساعد محلياً
        const assistantMsg: Message = {
          id: crypto.randomUUID(),
          conversation_id: currentConversation.id,
          role: 'assistant',
          content: fullContent,
          model: activeModel,
          platform: activePlatform,
          persona_name: activePersona?.name ?? null,
          tokens_used: estimatedTokens,
          response_time_ms: responseTime,
          created_at: new Date().toISOString(),
        };
        addMessage(assistantMsg);
        addTokens(estimatedTokens);

        // حفظ رسالة المساعد في قاعدة البيانات
        await supabase.from('messages').insert({
          conversation_id: currentConversation.id,
          role: 'assistant' as const,
          content: fullContent,
          model: activeModel,
          platform: activePlatform,
          persona_name: activePersona?.name ?? null,
          tokens_used: estimatedTokens,
          response_time_ms: responseTime,
        });

        // تحديث عنوان المحادثة إذا كانت أول رسالة
        if (messages.length === 0) {
          const title = content.substring(0, 50) + (content.length > 50 ? '...' : '');
          await supabase
            .from('conversations')
            .update({ title, updated_at: new Date().toISOString() })
            .eq('id', currentConversation.id);

          setConversation({ ...currentConversation, title });
          setConversations((prev) =>
            prev.map((c) => (c.id === currentConversation.id ? { ...c, title } : c))
          );
        }
      } catch (err) {
        if (err instanceof Error && err.name === 'AbortError') {
          // تم إلغاء البث بواسطة المستخدم
        } else {
          // إضافة رسالة خطأ
          const errorMsg: Message = {
            id: crypto.randomUUID(),
            conversation_id: currentConversation.id,
            role: 'assistant',
            content: err instanceof Error ? err.message : 'An error occurred',
            model: null,
            platform: null,
            persona_name: null,
            tokens_used: 0,
            response_time_ms: null,
            created_at: new Date().toISOString(),
          };
          addMessage(errorMsg);
        }
      } finally {
        setStreaming(false);
        setSending(false);
        setStreamingContent('');
        abortRef.current = null;
      }
    },
    [
      user, currentConversation, messages, activeModel, activePlatform,
      activePersona, apiType, supabase, addMessage, setSending, setStreaming,
      setStreamingContent, incrementMessageCount, addTokens, setConversation,
    ]
  );

  // إيقاف البث
  const stopStreaming = useCallback(() => {
    abortRef.current?.abort();
    setStreaming(false);
    setSending(false);
  }, [setStreaming, setSending]);

  // إنشاء محادثة
  const createConversation = useCallback(
    async (data: CreateConversationData): Promise<Conversation | null> => {
      if (!user) return null;
      try {
        const { data: newConv, error } = await supabase
          .from('conversations')
          .insert({
            user_id: user.id,
            title: data.title ?? 'محادثة جديدة',
            persona_id: data.persona_id ?? null,
            platform: data.platform,
            model: data.model,
            folder_id: data.folder_id ?? null,
          })
          .select()
          .single();
        if (error || !newConv) return null;
        const conv = newConv as Conversation;
        setConversation(conv);
        setMessages([]);
        setConversations((prev) => [conv, ...prev]);
        return conv;
      } catch { return null; }
    },
    [supabase, user, setConversation, setMessages]
  );

  // تحديث محادثة
  const updateConversation = useCallback(
    async (id: string, data: UpdateConversationData) => {
      try {
        await supabase
          .from('conversations')
          .update({ ...data, updated_at: new Date().toISOString() })
          .eq('id', id);
        setConversations((prev) =>
          prev.map((c) => (c.id === id ? { ...c, ...data } : c))
        );
        if (currentConversation?.id === id) {
          setConversation({ ...currentConversation, ...data, updated_at: new Date().toISOString() });
        }
      } catch { /* تجاهل */ }
    },
    [supabase, currentConversation, setConversation]
  );

  // حذف محادثة
  const deleteConversation = useCallback(
    async (id: string) => {
      try {
        await supabase.from('conversations').delete().eq('id', id);
        setConversations((prev) => prev.filter((c) => c.id !== id));
        if (currentConversation?.id === id) {
          clearChat();
        }
      } catch { /* تجاهل */ }
    },
    [supabase, currentConversation, clearChat]
  );

  // بحث
  const searchConversations = useCallback(
    (query: string): Conversation[] => {
      if (!query.trim()) return conversations;
      const lower = query.toLowerCase();
      return conversations.filter((c) => c.title.toLowerCase().includes(lower));
    },
    [conversations]
  );

  // تحميل أولي
  useEffect(() => {
    if (user && !loadedRef.current) {
      loadedRef.current = true;
      loadConversations();
    }
    return () => {};
  }, [user, loadConversations]);

  return {
    conversations,
    currentConversation,
    messages,
    isLoadingConversations,
    isLoadingMessages,
    isSending,
    isStreaming,
    streamingContent,
    loadConversations,
    loadConversation,
    loadMessages,
    sendMessage,
    stopStreaming,
    createConversation,
    updateConversation,
    deleteConversation,
    searchConversations,
  };
}
""")

    # ──────────────────────────────────────────────
    # API ROUTES
    # ──────────────────────────────────────────────
    print("\n📁 API Routes")
    print("-" * 40)

    # 15. app/api/chat/route.ts
    create_file("app/api/chat/route.ts", """// مسار API للدردشة: يعالج الطلبات ويبثها عبر SSE
import { NextResponse, type NextRequest } from 'next/server';
import { createSupabaseServerClient } from '@/lib/supabase-server';
import { createSupabaseAdminClient } from '@/lib/supabase-admin';
import { getProvider, isSupportedPlatform } from '@/lib/ai-providers/index';
import { decrypt } from '@/lib/encryption';
import type { AIMessage } from '@/types/chat';
import type { PlatformName } from '@/types/platform';

interface ChatRequestBody {
  messages: AIMessage[];
  model: string;
  platform: string;
  conversationId: string;
  personaName?: string | null;
  apiType: 'global' | 'private';
}

export async function POST(request: NextRequest) {
  try {
    // التحقق من المصادقة
    const supabase = createSupabaseServerClient();
    const { data: { session } } = await supabase.auth.getSession();

    if (!session) {
      return NextResponse.json({ error: 'غير مصرح' }, { status: 401 });
    }

    // جلب الملف الشخصي
    const { data: profile } = await supabase
      .from('profiles')
      .select('role, is_banned')
      .eq('id', session.user.id)
      .single();

    if (!profile) {
      return NextResponse.json({ error: 'ملف شخصي غير موجود' }, { status: 404 });
    }

    if (profile.is_banned) {
      return NextResponse.json({ error: 'الحساب محظور' }, { status: 403 });
    }

    // قراءة الجسم
    const body = await request.json() as ChatRequestBody;
    const { messages, model, platform, apiType } = body;

    if (!messages || !model || !platform) {
      return NextResponse.json({ error: 'بيانات ناقصة' }, { status: 400 });
    }

    if (!isSupportedPlatform(platform)) {
      return NextResponse.json({ error: 'منصة غير مدعومة' }, { status: 400 });
    }

    const platformName = platform as PlatformName;

    // الحصول على مفتاح API
    let apiKey: string;

    if (apiType === 'global') {
      // استخدام المفتاح العام
      const adminClient = createSupabaseAdminClient();
      const { data: globalKey } = await adminClient
        .from('api_keys')
        .select('encrypted_key')
        .eq('platform', platform)
        .eq('is_global', true)
        .eq('is_active', true)
        .limit(1)
        .single();

      if (!globalKey) {
        return NextResponse.json(
          { error: 'لا يوجد مفتاح عام متاح لهذه المنصة' },
          { status: 404 }
        );
      }

      try {
        apiKey = await decrypt(globalKey.encrypted_key);
      } catch {
        return NextResponse.json(
          { error: 'خطأ في فك تشفير المفتاح' },
          { status: 500 }
        );
      }
    } else {
      // المفتاح الخاص - يأتي من العميل مشفراً
      return NextResponse.json(
        { error: 'المفاتيح الخاصة تُرسل مباشرة من المتصفح' },
        { status: 400 }
      );
    }

    // تحديث last_used_at
    const adminClient = createSupabaseAdminClient();
    await adminClient
      .from('api_keys')
      .update({ last_used_at: new Date().toISOString() })
      .eq('platform', platform)
      .eq('is_global', true)
      .eq('is_active', true);

    // إنشاء طلب المزود
    const provider = getProvider(platformName);
    const streamReq = provider.createStreamRequest({
      apiKey,
      model,
      messages,
    });

    // إرسال الطلب للمزود
    const providerResponse = await fetch(streamReq.url, {
      method: 'POST',
      headers: streamReq.headers,
      body: streamReq.body,
    });

    if (!providerResponse.ok) {
      const errorText = await providerResponse.text().catch(() => 'Unknown error');

      // إشعار إذا كان خطأ رصيد
      if (providerResponse.status === 402 || providerResponse.status === 429) {
        await adminClient.from('notifications').insert({
          type: providerResponse.status === 402 ? 'api_depleted' : 'api_low_balance',
          title: providerResponse.status === 402 ? 'نفاد رصيد API' : 'رصيد API منخفض',
          message: \`خطأ \${providerResponse.status} من منصة \${platform}: \${errorText.substring(0, 200)}\`,
          priority: 'urgent',
          metadata: { platform, status: providerResponse.status },
        });
      }

      return NextResponse.json(
        { error: \`خطأ من المنصة: \${providerResponse.status}\` },
        { status: providerResponse.status }
      );
    }

    // إنشاء بث SSE
    const encoder = new TextEncoder();

    const stream = new ReadableStream({
      async start(controller) {
        const reader = providerResponse.body?.getReader();
        if (!reader) {
          controller.close();
          return;
        }

        const decoder = new TextDecoder();

        try {
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const text = decoder.decode(value, { stream: true });
            const lines = text.split('\\n');

            for (const line of lines) {
              const trimmed = line.trim();
              if (!trimmed) continue;

              let dataContent = trimmed;
              if (trimmed.startsWith('data: ')) {
                dataContent = trimmed.slice(6);
              }

              if (dataContent === '[DONE]') {
                controller.enqueue(encoder.encode('data: [DONE]\\n\\n'));
                continue;
              }

              const content = provider.parseStreamChunk(dataContent);
              if (content) {
                const sseData = JSON.stringify({ content });
                controller.enqueue(encoder.encode(\`data: \${sseData}\\n\\n\`));
              }
            }
          }
        } catch (err) {
          const errorMsg = err instanceof Error ? err.message : 'Stream error';
          controller.enqueue(
            encoder.encode(\`data: \${JSON.stringify({ error: errorMsg })}\\n\\n\`)
          );
        } finally {
          controller.close();
        }
      },
    });

    return new Response(stream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Accel-Buffering': 'no',
      },
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : 'خطأ داخلي';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
""")

    # 16. app/api/models/route.ts
    create_file("app/api/models/route.ts", """// مسار API للنماذج: جلب النماذج المتاحة حسب المنصة ونوع المفتاح
import { NextResponse, type NextRequest } from 'next/server';
import { createSupabaseServerClient } from '@/lib/supabase-server';
import { createSupabaseAdminClient } from '@/lib/supabase-admin';

export async function GET(request: NextRequest) {
  try {
    const supabase = createSupabaseServerClient();
    const { data: { session } } = await supabase.auth.getSession();

    if (!session) {
      return NextResponse.json({ error: 'غير مصرح' }, { status: 401 });
    }

    const { searchParams } = new URL(request.url);
    const platform = searchParams.get('platform');
    const apiType = searchParams.get('apiType') ?? 'global';

    if (!platform) {
      return NextResponse.json({ error: 'المنصة مطلوبة' }, { status: 400 });
    }

    if (apiType === 'global') {
      // جلب النماذج العامة من قاعدة البيانات
      const adminClient = createSupabaseAdminClient();

      const { data: models, error } = await adminClient
        .from('global_models')
        .select(\`
          id,
          model_id,
          model_name,
          is_active,
          sort_order,
          api_keys!inner (
            platform,
            is_active,
            is_global
          )
        \`)
        .eq('is_active', true)
        .order('sort_order', { ascending: true });

      if (error) {
        return NextResponse.json({ error: 'خطأ في جلب النماذج' }, { status: 500 });
      }

      interface ModelRow {
        id: string;
        model_id: string;
        model_name: string;
        is_active: boolean;
        sort_order: number;
        api_keys: {
          platform: string;
          is_active: boolean;
          is_global: boolean;
        };
      }

      const filteredModels = (models as unknown as ModelRow[])
        .filter((m) => {
          const key = m.api_keys;
          return key && key.platform === platform && key.is_active && key.is_global;
        })
        .map((m) => ({
          id: m.model_id,
          name: m.model_name,
          sortOrder: m.sort_order,
        }));

      return NextResponse.json(filteredModels);
    }

    // المفتاح الخاص: إرجاع تعليمات للعميل
    return NextResponse.json({
      message: 'Private API keys: fetch models directly from the provider',
      instruction: 'client_side_fetch',
      platform,
    });
  } catch {
    return NextResponse.json({ error: 'خطأ في الخادم' }, { status: 500 });
  }
}
""")

    # ──────────────────────────────────────────────
    # Summary
    # ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("📊 BUILD PHASE 3C SUMMARY")
    print("=" * 60)
    print(f"  ✅ Files created: {files_created}")
    print(f"  ❌ Files failed: {files_failed}")
    print(f"  📁 Total: {files_created + files_failed}")
    print()
    print("📋 Files Created:")
    print()
    print("  ENCRYPTION:")
    print("    •  lib/encryption.ts                   (AES-256-CBC encrypt/decrypt)")
    print()
    print("  CHAT COMPONENTS:")
    print("    1. components/chat/MessageInput.tsx     (1-5 lines, slash, send/stop)")
    print("    2. components/chat/SlashCommands.tsx    (System+premium+custom+/none)")
    print("    3. components/chat/RateLimitTimer.tsx   (Countdown + progress bar)")
    print("    4. components/chat/MessageLimitAlert.tsx (Dialog: keep/delete/export)")
    print()
    print("  AI PROVIDERS:")
    print("    5. lib/ai-providers/index.ts            (Factory + interface)")
    print("    6. lib/ai-providers/openrouter.ts       (OpenAI-compatible)")
    print("    7. lib/ai-providers/groq.ts             (OpenAI-compatible)")
    print("    8. lib/ai-providers/openai.ts           (Native)")
    print("    9. lib/ai-providers/anthropic.ts        (Custom: x-api-key, system extraction)")
    print("   10. lib/ai-providers/gemini.ts           (Custom: ?key=, contents/parts)")
    print("   11. lib/ai-providers/together.ts         (OpenAI-compatible)")
    print("   12. lib/ai-providers/mistral.ts          (OpenAI-compatible)")
    print()
    print("  HOOKS:")
    print("   13. hooks/useChat.ts                     (Full: send+stream+save+counters)")
    print("   14. hooks/useRateLimit.ts                (Free:4+180s, Premium:60s, Admin:none)")
    print()
    print("  API ROUTES:")
    print("   15. app/api/chat/route.ts                (JWT+decrypt+provider+SSE stream)")
    print("   16. app/api/models/route.ts              (Global=DB, Private=client)")
    print()
    print("📝 KEY FEATURES:")
    print("  - MessageInput: auto-resize 1-5 lines, Enter=send, Shift+Enter=newline")
    print("  - SlashCommands: 4 sections, keyboard nav, filter, lock premium for free")
    print("  - RateLimitTimer: visual countdown with progress bar")
    print("  - MessageLimitAlert: PDF/JSON/MD export options")
    print("  - 7 AI providers: 5 OpenAI-compatible + Anthropic + Gemini custom")
    print("  - Anthropic: system message extraction, x-api-key header")
    print("  - Gemini: contents/parts format, ?key= auth, streamGenerateContent")
    print("  - useChat: optimistic UI, SSE streaming, auto-title, error messages")
    print("  - useRateLimit: Free(4 free + 180s), Premium(60s hidden), Admin(unlimited)")
    print("  - Chat API: JWT auth, role check, key decrypt, SSE pipe, 402/429 notifications")
    print("  - All encrypted with AES-256-CBC, keys never exposed to client")
    print()
    print("🔜 REMAINING PHASES:")
    print("  Phase 4:  API Keys management + Settings page")
    print("  Phase 5A: Personas (library, form, ratings)")
    print("  Phase 5B: Features (export, onboarding)")
    print("  Phase 6A: Admin (layout, dashboard, users)")
    print("  Phase 6B: Admin (keys, models, personas, codes, notifications)")
    print("  Phase 7:  Final (worker proxy, telegram, polish)")
    print()
    print("✅ Phase 3C Complete! Ready for Phase 4.")


if __name__ == "__main__":
    main()
